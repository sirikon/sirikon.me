---
title: Mixing networks in Docker Compose
date: 2024-04-13 17:15
---

Turns out Docker Compose is pretty lazy and rigid when dealing with networks.

If you create a Docker container and join it to a bridge (default) network, the container's ID and name will resolve to the container's IP address in Docker's internal DNS server.

On top of that, Docker Compose will add the service name to the DNS server. **No matter what**. `hostname` doesn't replace the service name, just adds another name that resolves to the same thing. [I can point you to the exact line in the code](https://github.com/docker/compose/blob/b032999f06b3e18036f6777e121093f38a3ce627/pkg/compose/create.go#L415).

All these DNS names are added to **every network the container joins**, and you can't prevent that.

And that makes a funny scenario if you're trying to connect two projects. Imagine a escenario with these services:

- Project `alpha`
  - `web`: calls to `api`
  - `api`: calls to `db` and `beta`'s `api`
  - `db`
- Project `beta`
  - `api`: calls to `db`
  - `db`

If you connect `beta`'s `api` service to `alpha`'s network and `alpha`'s `web` makes a request to `api`, who will respond? Well, both `api`s from `alpha` and `beta` are registered at the DNS name `api`.

To prevent any problems, you would need to create a new network, include both `api`s to it with aliases like `alpha.api` and `beta.api` and make sure that `alpha`'s `api` is doing requests to the name `beta.api`, so it doesn't potentially call to itself. This way, you need to be aware of the potential name collissions in just one service, not many.

In summary: To connect two services from two different projects, create a third network and join just these two services, or confusing shit will happen.
