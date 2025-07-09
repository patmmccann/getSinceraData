Get Started with OpenSincera API
OpenSincera is a media telemetry service provided free of charge by The Trade Desk. It leverages rich advertising metadata from Sincera to deliver detailed insights into advertiser quality and the digital advertising supply chain. This service provides access to comprehensive metadata from more than 350,000 publishers, offering granular information about environments, content, configurations, and devices where ads run across the open internet.
Since Sincera doesn't own or operate media, it remains neutral and helps gain objective insight into the quality and value of ad inventory on the open internet. The platform delivers objective quality metrics such as ads-to-content ratio (A2CR), page weight, average ads in view, and ad refresh rate. For more details on benefits and features, see OpenSincera.
With its easy-to-use API, anyone in the ad industry can build custom solutions to bring greater transparency to the ecosystem by seamlessly integrating this data into their platforms. To help you get started, the following sections outline the API requirements and provide guidelines, examples, and FAQs.
NOTE: OpenSincera is in beta, giving you early access to test the API before its general availability release. During this period, you might encounter breaking changes and intermittent performance issues. Please report any issues or send questions to hello@sincera.io. A representative will respond as soon as possible.
Create Your OpenSincera Account
IMPORTANT: You must use a company email address to sign up. We don't accept generic email providers like Gmail.
To access the OpenSincera API, you must sign up for OpenSincera by doing the following:
1.	Go to the Sincera Create Your Account page.
2.	Fill out the form using your company email address.
3.	Confirm your account through the verification email.
Now you can retrieve your API token and access free publisher metadata from OpenSincera.
Retrieve Your API Token
To use the OpenSincera API, get an OpenSincera API bearer token by doing the following:
1.	On the OpenSincera website, click Sign In.
2.	Log in to your OpenSincera account.
3.	At the top-right, click your name and select Profile from the dropdown menu.
4.	In the API Key field in the Personal Information section, copy your API token.
Now you can use the token for making API calls.
Get Ecosystem Data
With your OpenSincera API token, you can retrieve comprehensive ecosystem data for OpenSincera. This includes ad media types, major prebid versions, common user modules, and more.
Request Syntax
Here's the syntax for retrieving general ecosystem data in cURL:
`curl -H "Authorization: Bearer AUTH_TOKEN_PLACEHOLDER" "https://open.sincera.io/api/ecosystem"`
For example:
`curl -H "Authorization: Bearer fak3T0k3n.12345.abcDEFGHIJKLMNOPQRST_uvwxYZ" "https://open.sincera.io/api/ecosystem"`
Response Object
The OpenSincera API returns a response object with comprehensive ecosystem metadata. The following is a sample response.
```
{
    "date": "2025-06-04",
    "updated_at": "2025-06-04T01:24:40.332Z",
    "known_adsystems": 989,
    "adsystem_ecosystem": {
        "Ad Network": 229,
        "Walled Garden": 22,
        "Header Wrapper": 6
    },
    "global_gpids": 3634159,
    "pbjs_ad_unit_media_types": {
        "pos": "20",
        "video": "12177755",
        "banner": "30140808",
        "native": "1183354",
        "slider": "6757",
        "bidders": "31",
        "display": "5",
        "ortb2Imp": "12",
        "platform": "31"
    },
    "video_plcmt_pubs": 43239,
    "pubs_with_gpid": 89084,
    "pbjs_major_versions": [
        ["s.x", "1158"],
        ["9.x", "75457"],
        ["8.x", "37706"]
    ],
    "global_policies": 61119934,
    "recently_updated_publishers": [1369, 329916, 67553],
    "header_wrappers": {
        "Prebid.org": 105479,
        "Amazon": 82569,
        "PubMatic": 73866
    },
    "avg_user_modules_deployed": 6.137288594020969,
    "avg_audience_providers_deployed": 1.533262827510917,
    "sincera_ecosystem_size": 367635,
    "webrisk_flagged_publishers": 786,
    "adult_domains": 3728,
    "topics_opt_outs": 21324
}
```
The following table lists the properties in the response object.
Property Name	Description
date	The date when the data was retrieved.
updated_at	The timestamp for when the data was last updated.
known_adsystems	The number of ad systems in the Sincera ecosystem.
adsystem_ecosystem	A breakdown of known ad systems by platform type and count.
global_gpids	The number of global placement identifiers (GPIDs) found by Sincera.
pbjs_ad_unit_media_types	A breakdown of Prebid ad unit types found on publisher domains.
video_plcmt_pubs	The number of publishers with video placement (video.plcmt) signals found.
pubs_with_gpid	The number of publishers with GPIDs found.
header_wrappers	A breakdown of header wrappers found across the Sincera publisher ecosystem, categorized by ad system.
pbjs_major_versions	A breakdown of Prebid wrapper versions found across the Sincera publisher ecosystem.
avg_user_modules_deployed	The average number of user modules found in Prebid wrappers across the Sincera publisher ecosystem.
avg_audience_providers_deployed	The average number of audience providers deployed by publishers.
global_policies	The number of policies (ads.txt entries) recorded by Sincera.
recently_updated_publishers	An array of publishers updated within the last 24 hours as detected by Sincera, identified by their publisher ID.
sincera_ecosystem_size	The number of publishers in the Sincera ecosystem.
webrisk_flagged_publishers	The number of publishers flagged by Google Web Risk in the Sincera ecosystem.
adult_domains	The number of publishers flagged for adult content in the Sincera ecosystem.
topics_opt_outs	The number of publishers opting out of specific topics in the Sincera ecosystem.
Get Publisher Metadata
With your OpenSincera API token, you can retrieve publisher information for a specific ID or domain. Here's what you need to know about using the API, including rate limits, token restrictions, and formatting requirements:
•	Use the base path https://open.sincera.io/api.
•	You can retrieve publisher IDs from the OpenSincera UI. For example, the publisher ID for Business Insider is 1.
•	Exclude the protocol and path from the publisher's domains. For example, https://www.businessinsider.com should be businessinsider.com.
•	The rate limit is set at 5000 requests within a rolling 24-hour period and 45 requests per rolling minute. These limits are subject to change.
IMPORTANT: Attempting to bypass rate limits by using multiple tokens on the same system results in permanent suspension from the platform.
The following sections explain the request syntax in cURL and use Business Insider as a publisher in the examples. However, you can use this same information with any technology and get similar results.
For a Given Publisher ID
Here's the syntax for retrieving publisher information for a publisher ID. `curl -H "Authorization: Bearer AUTH_TOKEN_PLACEHOLDER" "https://open.sincera.io/api/publishers?id=PUBLISHER_ID_PLACEHOLDER"`
For example: `curl -H "Authorization: Bearer fak3T0k3n.12345.abcDEFGHIJKLMNOPQRST_uvwxYZ" "https://open.sincera.io/api/publishers?id=1"`
For a Given Publisher Domain
Here's the syntax for retrieving publisher information for a publisher domain.` curl -H "Authorization: Bearer AUTH_TOKEN_PLACEHOLDER" "https://open.sincera.io/api/publishers?domain=PUBLISHER_DOMAIN_PLACEHOLDER"`
For example:  `curl -H "Authorization: Bearer fak3T0k3n.12345.abcDEFGHIJKLMNOPQRST_uvwxYZ" "https://open.sincera.io/api/publishers?domain=businessinsider.com"`
Response Object
The OpenSincera API returns a response object with comprehensive publisher metadata, including the A2CR ratio, page weight, average ads in view, and ad refresh rate. The following is a sample response for a Business Insider request.
```
{
    "publisher_id": 1,
    "name": "Business Insider",
    "visit_enabled": true,
    "status": "available",
    "primary_supply_type": "web",
    "domain": "businessinsider.com",
    "pub_description": "Business Insider tells the global tech, finance, stock market, media, economy, lifestyle, real estate, AI and innovative stories you want to know.",
    "categories": [
        "General",
        "Business and Finance",
        "Technology & Computing",
        "Personal Finance",
        "Law",
        "Business",
        "Computing"
    ],
    "slug": "business-insider",
    "avg_ads_to_content_ratio": 0.20989,
    "avg_ads_in_view": 1.90454,
    "avg_ad_refresh": 64.395,
    "total_unique_gpids": 792,
    "id_absorption_rate": 0.244,
    "avg_page_weight": 27.8427,
    "avg_cpu": 254.6705,
    "total_supply_paths": 90,
    "reseller_count": 44,
    "owner_domain": "insider-inc.com",
    "updated_at": "2025-06-02T14:36:17.349Z"
}
```
The following table lists the properties in the response object.
Property Name	Description
publisher_id	The Sincera ID for the publisher. This matches the ID in the OpenSincera UI.
name	The name of the publisher.
visit_enabled	If set to true, indicates that Sincera visits the publisher regularly. The default value is true.
status	The status of the publisher's website as seen by OpenSincera synthetic users, which are simulated users that mimic typical consumer behavior online.
primary_supply_type	The type of platform used for the A2CR value. For example, web or ctv.
domain	The base domain for the publisher website.
pub_description	Sincera's description of the publisher, as shown on the OpenSincera platform.
categories	The Interactive Advertising Bureau (IAB) 3.0 Content Taxonomy categories and manually assigned categories for the publisher.
slug	The part of a URL that identifies a specific page on a website in a readable way. It comes after the domain and any directory structure. For example, open.sincera.io/publisher/businessinsider.
avg_ads_to_content_ratio	The A2CR (ads-to-content ratio) is the average of metrics that measure the percentage of pixels allocated to ads compared to those dedicated to content on a webpage. Sincera evaluates both the dimensions of the creatives and the ad slots, using the larger of the two values to calculate the A2CR. The value returned is an percentage. For example, 0.2 is 20%.
avg_ads_in_view	The average number of ads in view at the viewport level. Sincera calculates this by comparing the ad server functions or ad slot coordinates with a given viewport on the page.
avg_ad_refresh	The average time in seconds before an ad unit refreshes. Sincera monitors ad refresh timings across multiple ad servers.
total_unique_gpids	The total number of GPIDs, which are unique placement IDs specified by the publisher that remain unchanged across all supply-side platforms (SSPs).
id_absorption_rate	The identifier absorption rate, a metric developed by Sincera, measures how effectively SSPs append identifiers to their outgoing bid requests. It focuses on the success rate when an identifier is already present, not the overall enrichment rate. A higher score indicates that a larger proportion of real-time bidding (RTB) traffic includes user identifiers.
avg_page_weight	The average file size in MB for a given URL, which is a signal that inversely correlates with ad performance.
avg_cpu	The average CPU usage for a given URL, which is a signal that inversely correlates with ad performance. CPU usage is measured in seconds.
total_supply_paths	The total number of supply paths an ad takes from the advertiser to the publisher's website or app where it is displayed. It includes the series of intermediaries involved in the selling and delivery of the ad inventory, such as ad exchanges, SSPs, and other resellers.
reseller_count	The number of resellers associated with the publisher.
owner_domain	The owner domain listed in the publisher's ads.txt file.
updated_at	The most recent update to the publisher's statistics.
FAQs
The following is a list of frequently asked questions about OpenSincera.
Can I sign up for OpenSincera now?
No. OpenSincera is currently in a limited beta release and access is restricted to our initial group of beta users. If you have not contacted the Sincera team at hello@sincera.io or were not included in the first wave of beta invitations, you cannot sign up at this time. We are gradually expanding access, and those who have expressed interest will receive an email notification when access becomes available.
What is the pricing for OpenSincera?
The OpenSincera UI and API is free to use (with conditions) for any company in our industry. Even competitors of The Trade Desk.
Are there specific policies I should be aware of?
Do not engage in what is referred to as "data passthrough"—simply taking OpenSincera data and making the entire dataset 1-to-1 available for an audience. If OpenSincera data is used in an application, such as a reporting UI, you must state that the data source is OpenSincera in a reasonably discoverable (but not onerous or burdensome) way.
As an API user, take care not to misrepresent your metrics as OpenSincera metrics—or vice versa—within your applications. Avoid duplicating or creating similar metrics of well-known Sincera dimensions, such as the A2CR, which further blur the line between your data and data from OpenSincera for your end users.
Can anyone sign up and use OpenSincera?
Yes. Anyone in the ad industry can sign up. OpenSincera has a graph of about 1,000 companies in digital advertising. Users from those companies can user their work email addresses to sign up and access OpenSincera.
Users outside of these companies can still join. However, their accounts and companies are subject to a short review period.
Why can't I join with a Gmail or generic email address?
Blocking Gmail and generic email addresses prevents anonymous and malicious attempts to access OpenSincera data.
If I have a legacy Sincera account, does that mean I already have an OpenSincera account?
Users of the legacy Sincera application (app.sincera.io) will have their accounts ported over. If you've haven't created an account with us in the past, you can create a new account at the Sincera Create Your Account page.
What happens if I search for a domain OpenSincera does not currently track?
If the domain isn’t currently in the OpenSincera dataset, the API will return a 404 (Not Found) HTTP response code.
What should I do if my bearer token is not working?
Double-check that you're using the correct token and that it's formatted properly. Make sure it matches exactly what was issued, with no extra spaces or characters. For help, contact hello@sincera.io.
I need more data. Can my rate limit be increased?
During the closed beta, rate limits are fixed for all users and cannot be adjusted. These limits may be revised when the API becomes publicly available.
What does A2CR mean?
The A2CR (ads-to-content ratio) is the average of metrics that measure the percentage of pixels allocated to ads compared to those dedicated to content on a webpage. Sincera evaluates both the dimensions of the creative and the ad slot, using the larger of the two values to calculate the A2CR. The value returned is a percentage. For example, 0.2 is 20%.
Can you meet with me to discuss OpenSincera?
The response and interest in OpenSincera have been extremely high, which is humbling, but we're super focused on building our application. We can't accommodate individual meetings before launching the beta, but we're happy to discuss meetings afterwards.
If you need timely feedback, we would love any thoughts at `hello@sincera.io`.

