mongo-spade-replicate
=====================

This is multi-agent system for distribued Mongo DB data replication. You can define you own rules for replication by defining network topology of data replication.

### How to run?

First install Mongo on each server on which you want to run ``mongo-spade-replicate``.

Then install deps:

```
sudo pip install -r req.txt
```

Then you need edit ``config.py`` on each server in something like this:

```python
connected = {
    # host_name source : [[agentName_receiver, spade_platform_ip]]
    'host1': [['host2_receiver', HOST_SPADE_IP]],
    'host2': [['host1_receiver', HOST_SPADE_IP], ['host3_receiver', HOST_SPADE_IP]],
    'host3': [['host1_receiver', HOST_SPADE_IP]]
}
```

You see that key is hostname of server on which is Mongo instance, and value is list of servers where we want to replicate data when data change occurs in served with hostname specified in key. This is important part, because with this you actually define rules on which data replication works for your case. You can edit this for your own needs. Note that each destination part must have ``_receiver`` in name, because that is name of agent on destination host which is responsabile for accepting incomming data.

You also need to say where is ``SPADE`` platform:

```
# example
HOST_SPADE_IP = '192.168.1.1'
```

At the end, on host with that IP run:

```
# IMPORTANT: change this IP according to IP defined in HOST_SPADE_IP var.
configure.py 192.168.1.1
```

At the end on each host run:
```
python main.py
```

Please see content of ``main.py`` script and look at the python interface in ``event.mongo_event`` module. There you will find ``trigger_add``, ``trigger_update`` and ``trigger_delete`` methods which are entry point of mongo replication with ``SPADE`` platform. There is example of using this methods in ``models.test`` module.

### Questions

Feel free to contact me on pusic007@gmail.com

### Contributions

Feel free to send pull request or open issue.
