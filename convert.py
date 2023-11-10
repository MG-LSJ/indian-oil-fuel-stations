from bs4 import BeautifulSoup
import geojson


maxPages = 6145
features = []


class NoOutletsFoundException(Exception):
    pass


def parsePage(pageContent):
    soup = BeautifulSoup(pageContent, "html5lib")

    if soup.find("div", attrs={"class": "no-outlets"}):
        raise NoOutletsFoundException("No outlets found")

    stores = soup.find("div", attrs={"class": "outlet-list"})

    for store in stores.find_all("div", attrs={"class": "store-info-box"}):
        lat = (
            store.find("input", attrs={"class": "outlet-latitude"}).attrs["value"] or 0
        )
        lng = (
            store.find("input", attrs={"class": "outlet-longitude"}).attrs["value"] or 0
        )
        name = (
            store.find("li", attrs={"class": ""})
            .find("div", attrs={"class": "info-text"})
            .text
        ).strip()
        address = (
            store.find("li", attrs={"class": "outlet-address"})
            .find("div", attrs={"class": "info-text"})
            .get_text(separator=" ")
        ).strip()
        phone = (
            store.find("li", attrs={"class": "outlet-phone"})
            .find("div", attrs={"class": "info-text"})
            .text
        ).strip()
        timings = (
            store.find("li", attrs={"class": "outlet-timings"})
            .find("div", attrs={"class": "info-text"})
            .text
        ).strip()
        address, areacode = [x.strip() for x in address.split(" - ")]
        url = (
            store.find("li", attrs={"class": "outlet-name"})
            .find("div", attrs={"class": "info-text"})
            .find("a")
            .attrs["href"]
        ).strip()

        features.append(
            geojson.Feature(
                geometry=geojson.Point((float(lng), float(lat))),
                properties={
                    "name": name,
                    "address": address,
                    "areacode": areacode,
                    "phone": phone,
                    "timings": timings,
                    "url": url,
                },
            )
        )


for i in range(1, maxPages + 1):
    try:
        with open(f"responses/{i}.html", "r") as f:
            parsePage(f.read())
    except NoOutletsFoundException:
        print(f"No outlets found on page {i}")
    except:
        print(f"Error parsing page {i}")


featureCollection = geojson.FeatureCollection(features)
with open("indian_oil_fuel_stations.geojson", "w") as f:
    geojson.dump(featureCollection, f)
