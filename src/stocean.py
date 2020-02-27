import requests


class Comic:
    def __init__(self, name, date, image, description, alt):
        self.name = name
        self.date = date
        self.image = image
        self.description = description
        self.alt = alt
    def dict(self):
        return {
            'name': self.name,
            'date': self.date,
            'image': self.image,
            'description': self.description,
            'alt': self.alt
        }


def rainCheck():
    # Get status of Pebbleyeet's page
    return int(str(requests.get("http://www.stonetoss.com")).split("[")[1].split("]>")[0])


def grabLatest():
    # Get webpage
    html = str(requests.get("http://stonetoss.com").content)
    # Get name of comic
    name = html.split("rel=\"bookmark\">")[1].split("</a>")[0]
    # Get description
    description = html.split("class=\"post-content\">")[1].split("<p>")[1].split("</p>")[0]
    # Get date comic was published
    date = html.split("<time datetime=\"")[1].split("T")[0]
    # Get url of image
    image = html.split("<div id=\"comic\">")[1].split("<img src=\"")[1].split("?fit=")[0]
    # Get alt text
    alt = html.split("<div id=\"comic\">")[1].split("alt=\"")[1].split("\" title=\"")[0]
    # Create comic class
    st = Comic(name, date, image, description, alt)
    return st


def grabSpecific(com):
    # Parse the name into a URL
    # "Affirmative (Re)Action(ary)" -> "affirmative-(re)action(ary)"
    urlName = "-".join(com.split()).lower()
    # "affirmative-(re)action(ary)" -> "affirmative-reactionary"
    punctuation = "?/!@#$%^&*()[]{}|\\+=~`.,<>:;'\""
    for i in punctuation:
        urlName = "".join(urlName.split(i))
    urlName = "http://stonetoss.com/comic/%s/" % urlName

    # Create the comic class (almost same method as grabLatest())
    html = str(requests.get(urlName).content)
    name = html.split("rel=\"bookmark\">")[1].split("</a>")[0].split("<span class=\"screen-reader-text\">")[1].split(" published on </span>")[0]
    description = html.split("class=\"post-content\">")[1].split("<p>")[1].split("</p>")[0]
    date = html.split("<time datetime=\"")[1].split("T")[0]
    image = html.split("<div id=\"comic\">")[1].split("<img src=\"")[1].split("?fit=")[0]
    alt = html.split("<div id=\"comic\">")[1].split("alt=\"")[1].split("\" title=\"")[0]
    st = Comic(name, date, image, description, alt)
    return st


def grabArchives():
    # Get webpage
    res = []
    html = str(requests.get("http://stonetoss.com/archive/").content)
    archiveText = html.split("<div class=\"comic-archive-list-wrap\">")[1].split("<div style=\"clear:both;\">")[0].split("</div>")
    # Process webpage and get entries
    for i in range(len(archiveText) - 2):
        x = archiveText[i].split("Permanent Link: ")[1]
        l = archiveText[i].split("http://stonetoss.com/comic/")[1].split("\"")[0]
        res.append({'name': x.split("\">")[0], 'link': l.split("/")[0]})
    return res
