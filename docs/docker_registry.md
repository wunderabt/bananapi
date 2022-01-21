# Run a docker registry on the banana-pi

## Server setup

Install docker

```bash
sudo apt install docker.io
```

Create a self-signed cert that is valid for 10y

```bash
openssl req \
  -newkey rsa:4096 -nodes -sha256 -keyout certs/domain.key \
  -addext "subjectAltName = DNS:troi.fritz.box" \
  -x509 -days 3650 -out certs/domain.crt
```
  
When prompted for "name" enter the host name (e.g. `troi.fritz.box`)
  
Start the registry on that host. Note the two `-v ..` volume switches that use the certificate
created above and use a local drive to store the images.

```bash
sudo docker pull registry
sudo docker run -d \
  --restart=always \
  --name registry \
  -v /home/public/certs:/certs \
  -v /home/docker_registry:/var/lib/registry \
  -e REGISTRY_HTTP_ADDR=0.0.0.0:443 \
  -e REGISTRY_HTTP_TLS_CERTIFICATE=/certs/domain.crt \
  -e REGISTRY_HTTP_TLS_KEY=/certs/domain.key \
  -p 443:443 \
  registry:latest
```

## Client setup

copy the certificate to each client machine

```bash
sudo mkdir -p /etc/docker/certs.d/troi.fritz.box/
sudo cp /mnt/public/certs/domain.crt /etc/docker/certs.d/troi.fritz.box/ca.crt
```

test the registry

```bash
docker pull alpine
docker tag alpine:latest troi.fritz.box/apline:latest
docker push troi.fritz.box/apline:latest
```

## Rest-API

some [Rest-API](https://docs.docker.com/registry/spec/api/) examples

```
https://troi.fritz.box/v2/_catalog
https://troi.fritz.box/v2/ubapache/tags/list
```

### delete an image

enable deletion on the registry. Log into the running registry:
```bash
sudo docker exec -it <container> /bin/sh
```

and enable the deletion option
```bash
vi /etc/docker/registry/config.yml
```

insert
```yaml
  delete:
    enabled: true
```
in the `storage:` section.

Restart docker `sudo service docker restart`


find the digest
```bash
curl -v --silent -H "Accept: application/vnd.docker.distribution.manifest.v2+json" -X GET https://troi.fritz.box/v2/vivado/manifests/latest | grep docker-content-digest
```

the digest can be used to delete the image
```bash
curl --silent -H "Accept: application/vnd.docker.distribution.manifest.v2+json" -X DELETE https://troi.fritz.box/v2/alpine/manifests/sha256:xxxxx
```

### garbage collect

```bash
sudo docker exec -it <container> /bin/sh
registry garbage-collect -m /etc/docker/registry/config.yml
```
