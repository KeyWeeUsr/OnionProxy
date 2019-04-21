# OnionProxy

Imagine you have a spare computer or a virtual private server or you know
someone who would host something for you and let's say you want to access
a website but you don't want to leave a trace on a specific device.

Now let's scale it a bit and say you have multiple websites, multiple devices
and you want to be able to access even non-clearnet stuff.

Common steps for that would perhaps be getting some tool for privacy for each
of the client devices. But what if a clearnet website breaks your plans by just
not being compatible with the privacy solution? Let's use Tor as an example.

Imagine you want to access one of [these websites](
https://trac.torproject.org/projects/tor/wiki/org/doc/ListOfServicesBlockingTor
)([onion link](
http://ea5faa5po25cf7fb.onion/projects/tor/wiki/org/doc/ListOfServicesBlockingTor
)). Well, you can't. You'll either need to visit the page without Tor, or
sacrifice some of "your" privacy to stay hidden.

There are multiple situations when you need to stay hidden whether it's
censorship, personal interests or whatever. With this tool you can create
your own proxy which is not publicly visible nor easily guessable (.onion
address) to a server (website, DB, etc) that either completely blocks Tor
traffic or to a server that allows access only from a specific IP.

### Ideas

Since this allows you to create proxies and each proxy is a separate service,
you can easily wrap third-party websites (if they allow you to do so in
ToC/ToS) into services, therefore create your own network of onions.

Some ideas with that in mind:

* Public institutions running onion proxies
* Onion addresses for your personal websites/servers
* Separate network of proxies in a non-censorship country used in a country
  with common censorship
* Onion proxy to access a server that limits the traffic to a specific IP
  (proxy running on that machine) while traveling/using VPN/having burner
  device.

### Limits

Currently the tool allows proxying only for clearnet websites, a single domain,
therefore websites with resources distributed across multiple domains, let's
say Wikipedia

    https://wikimedia.org
    https://meta.wikimedia.org
    https://upload.wikimedia.org
    https://wikipedia.org
    https://en.wikipedia.org
    ...

proxying would mean creating a proxy for each of the domains and redirect all
of the locations to the appropriate sub-locations (and rewrite response bodies,
rewrite Host, Location and perhaps other headers to make it load properly)
or even own onion services. Solutions such as this cause more work than they
are useful, therefore depending on the use-case it might be more comfortable to
just run an exit node. For such case though you allow everyone to access your
server due to the inclusion of your server to the network as the node anyone
can visit any page from.

See the sample config for Wikipedia in the ``confs`` folder.

### Run

1. Get [Docker](https://www.docker.com/get-started)
2. Get Tor Browser
   [via torproject.org](https://www.torproject.org/download/download-easy.html.en),
   [via email](mailto://gettor@torproject.org),
   [via twitter](https://twitter.com/get_tor)
3. ``git clone https://github.com/KeyWeeUsr/OnionProxy``
4. Create a ``proxies.txt`` template.
5. Run the ``./opctl.sh --recreate`` (MacOS or GNU/Linux) to create Docker .yml
6. Get your .onion addresses: ``./opctl.sh --hostnames``
7. Navigate to the .onion address in the Tor Browser
8. Enjoy

### Warning

#### Keys

The keys for the .onion services are stored in separate volumes named by the
``proxies.txt`` template. Once you remove such volume or rename the service,
the stored key is no longer used. If by any chance you only rename the service
you can rename it back to get the same address or copy the old key from the
old volume to the new one.

Once you delete the Docker volume with the keys, your .onion address is gone.

#### Security

Once you access the .onion proxy **everything is unsecure**. You can see the
default remote IP (``127.0.0.1`` by default), **the whole** incomming request
and you can log, manipulate and prevent the traffic (as with any other proxy!)
therefore if you decide to deploy it, be sure the host is safe both system-wise
(secure server, firewall, all that) and location-wise. :)
