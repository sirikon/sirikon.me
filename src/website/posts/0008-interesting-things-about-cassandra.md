---
title: Interesting things about Cassandra
date: 2024-04-17 21:45
---

I'm super late to the Cassandra hype party of _many_ years ago, but I never had any interest in it until now. Now at work we're considering it, and to make an educated decission we need to study it a bit.

## Masterless

The key trick of Cassandra is the "Partition Key", which is a set of columns you choose in a table to say "these are the columns used to compute a hash and decide where the row is managed".

Imagine having a Cassandra cluster (or [ring](https://cassandra.apache.org/doc/latest/cassandra/architecture/dynamo.html#consistent-hashing-using-a-token-ring)) with many nodes. If you send a request to Cassandra to write some new data, all the information Cassandra needs to decide which node handles the request is:

- The columns composing the Partition Key, which you're sending with the request.
- The nodes present in the ring (with some metadata, but not much).

There is no centralized lookup table with key ranges pointing to specific nodes. There isn't even a single node handling requests from clients, as any node can receive requests and know exactly where to relay them. This system splits read and write operations across the cluster with very little overhead.

That's what makes it "masterless", there is no actual leader in the cluster anywhere, which is something you would typically see in other databases.

## Kinda limited

The database is clearly designed to have partitions and nodes as independent as possible from each other. No operation requires close coordination of multiple nodes. If you make a request with `SELECT * FROM table`, you'll get all the information present from all nodes, aggregated, and not always necessarily in the same order. That's the maximum cross-node collaboration you'll get.

It supports SQL (actually, [CQL](https://cassandra.apache.org/doc/latest/cassandra/developing/cql/index.html)) but there are no `JOIN`s, no sub-queries, atomicity of multiple statements is only possible within the same partition key... the feature set is just a very minimal subset of what Postgres could offer, **which is fine**, because they're different databases for different purposes.

Don't get fooled by the fact that it supports something like SQL. As a colleague said very succintly: It's a glorified Key-Value store.

It provides a way to have widely distributed and non-related information (that you will never cross-reference) splitted in multiple nodes, being able to do basic read/write operations that a single node can handle in isolation, with strong replication and fault-tolerance.

## EDIT: Amazon Keyspaces

AWS's serverless Apache Cassandra offering. It's trash.

It has no support for secondary indexes, materialized views, logged batches or aggregates. Turns a limited option into a stupid one, because you could pick any eventually-consistent key-value store and achieve the same.

## Wraping up

If you're interested in reading more, [the official arquitecture docs are pretty good](https://cassandra.apache.org/doc/latest/cassandra/architecture/index.html).
