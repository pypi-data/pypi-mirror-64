import html
import re
from urllib.parse import urlparse, urlunparse, quote, unquote  # noqa: F401

# TODO
# replaced: parsed = mdurl.parse(url, True)
# but need to check these fixes from https://www.npmjs.com/package/mdurl:
#
# Parse url string. Similar to node's url.parse,
# but without any normalizations and query string parse.
#    url - input url (string)
#    slashesDenoteHost - if url starts with //, expect a hostname after it. Optional, false.
# Difference with node's url:

# No leading slash in paths, e.g. in url.parse('http://foo?bar') pathname is ``, not /
# Backslashes are not replaced with slashes, so http:\\example.org\ is treated like a relative path
# Trailing colon is treated like a part of the path, i.e. in http://example.org:foo pathname is :foo
# Nothing is URL-encoded in the resulting object,
# (in joyent/node some chars in auth and paths are encoded)
# url.parse() does not have parseQueryString argument
# Removed extraneous result properties: host, path, query, etc.,
# which can be constructed using other parts of the url.


#  ################# Copied from Commonmark.py #################

ENTITY = "&(?:#x[a-f0-9]{1,6}|#[0-9]{1,7}|[a-z][a-z0-9]{1,31});"
ESCAPABLE = "[!\"#$%&'()*+,./:;<=>?@[\\\\\\]^_`{|}~-]"
reBackslashOrAmp = re.compile(r"[\\&]")
reEntityOrEscapedChar = re.compile("\\\\" + ESCAPABLE + "|" + ENTITY, re.IGNORECASE)


def unescape_char(s):
    if s[0] == "\\":
        return s[1]
    else:
        return html.unescape(s)


def unescape_string(s):
    """Replace entities and backslash escapes with literal characters."""
    if re.search(reBackslashOrAmp, s):
        return re.sub(reEntityOrEscapedChar, lambda m: unescape_char(m.group()), s)
    else:
        return s


def normalize_uri(uri):
    return quote(uri.encode("utf-8"), safe=str("/@:+?=&()%#*,"))


##################


RECODE_HOSTNAME_FOR = ("http", "https", "mailto")


def normalizeLink(url):

    # parsed = urlparse(url)

    # if parsed.hostname:
    #     # Encode hostnames in urls like:
    #     # `http:#host/`, `https:#host/`, `mailto:user@host`, `#host/`
    #     #
    #     # We don't encode unknown schemas, because it's likely that we encode
    #     # something we shouldn't (e.g. `skype:name` treated as `skype:host`)
    #     #
    #     if (not parsed.scheme) or parsed.scheme in RECODE_HOSTNAME_FOR:
    #         try:
    #             parsed.hostname = punycode.toASCII(parsed.hostname)
    #         except Exception:
    #             pass
    # quote(urlunparse(parsed))
    return normalize_uri(unescape_string(url))


def normalizeLinkText(title):
    """Normalize autolinks """

    # parsed = urlparse(url)

    # if parsed.hostname:
    #     # Encode hostnames in urls like:
    #     # `http:#host/`, `https:#host/`, `mailto:user@host`, `#host/`
    #     #
    #     # We don't encode unknown schemas, because it's likely that we encode
    #     # something we shouldn't (e.g. `skype:name` treated as `skype:host`)
    #     #
    #     if (not parsed.protocol) or parsed.protocol in RECODE_HOSTNAME_FOR:
    #         try:
    #             parsed.hostname = punycode.toUnicode(parsed.hostname)
    #         except Exception:
    #             pass
    return unquote(unescape_string(title))  # unquote(urlunparse(parsed))


################################################################################
#
# This validator can prohibit more than really needed to prevent XSS. It's a
# tradeoff to keep code simple and to be secure by default.
#
# If you need different setup - override validator method as you wish. Or
# replace it with dummy function and use external sanitizer.
#

BAD_PROTO_RE = re.compile(r"^(vbscript|javascript|file|data):")
GOOD_DATA_RE = re.compile(r"^data:image\/(gif|png|jpeg|webp);")


def validateLink(url: str):
    """url should be normalized at this point, and existing entities are decoded."""
    url = url.strip().lower()
    return (
        (True if GOOD_DATA_RE.search(url) else False)
        if BAD_PROTO_RE.search(url)
        else True
    )
