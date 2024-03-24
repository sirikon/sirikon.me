---
title: Two WiFi access points. One SSID. It's okay
date: 2023-10-13 18:40
---

Having two WiFi ACs with the same SSID and password allows you to have the same configuration on two different locations. Connect to WiFi at home and at the office by configuring your devices just once. Convenient in some scenarios.

Having two WiFi ACs with the same SSID and password **close together** (like, at home), is a different story. Your mileage may vary, but it should be mostly fine.

There's no definitive answer to the question "will it work properly" because we're working out of the standard here, and it depends on each implementation, but some rough guidelines are:

- **There can be many ACs, but only one of them should act as a router**. This means: If you're repurposing an old WiFi router, disable its DHCP server and any other capability different from moving packets around and emitting WiFi.
- **Be sure that SSID, password and encryption protocol are exactly the same**. SSID and password are case sensitive, and some devices might use the encryption (WEP, WPA, WPA2...) as a clue to differentiate between ACs.
- **Make sure each AC is on a different channel**. This applies to any set of ACs really. This can be done manually by selecting a channel on each one, but I'm a lazy fuck so I prefer to leave them on "auto" and let them resolve their own problems like adult ACs.

How well will it work? **✨It depends✨**.

There might be some coverage overlap between ACs. For example: If you connected to the WiFi near AC #1 at your living room, and walked towards AC #2 in your bedroom, for the majority of devices it will stay connected to AC #1 **as long as there's any signal left**, meaning that you'll have poor WiFi connectivity and your phone will have no way of knowing there's another AC with a stronger signal right in front of him. Devices tend to find an alternative WiFi AC only when they're **completely** out of range.

In these scenarios: **Just turn off WiFi and turn it on again**. That should be enough for the device to pick up the AC with the strongest signal. (There's no actual need to turn off WiFi on your device for all this to work, but it might be the fastest way to disconnect from the existing network and force a re-scan of ACs).

It might be annoying if you're walking around the house with a Google Meet call because you'll be losing signal anyway, but it should be fine for the poor Roomba that needs to connect from every corner in your home that you decided to eat Cheetos in.

If all of this doesn't work, I'm sorry, pick a different SSID for each AC, buy a new AC with stronger signal, or get one of those fancy "Mesh WiFi" products that honestly I don't know how they work and won't investigate until I have the actual need.


*[AC]: Access Point
*[ACs]: Access Points
*[SSID]: Service Set IDentifier, or what anyone would refer to as the WiFi's "name".
*[DHCP]: Dynamic Host Configuration Protocol, the thing that assings IPs to devices connected to the network automatically.
