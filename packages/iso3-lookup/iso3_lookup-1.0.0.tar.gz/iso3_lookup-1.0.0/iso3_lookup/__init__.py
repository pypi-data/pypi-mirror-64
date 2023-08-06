from iso3_lookup.backend import Lookup

lkp = Lookup()


def get_iso3(country: str) -> str:
    """
    From a given country, return the iso3 code.

    Attributes
    ----------
    country : str
        name of country

    Returns
    -------
    str
        ISO3 code
    """
    return lkp.find_and_return_max("name", country, "alpha-3")


def get_country(iso3: str) -> str:
    """
    From a ISO3 code, return the country name.

    Attributes
    ----------
    iso3 : str
        ISO3 code

    Returns
    -------
    str
        country name
    """
    return lkp.find_and_return_max("alpha-3", iso3, "name")


def get_region(country: str) -> str:
    """
    From a given country, return the region name.

    Attributes
    ----------
    country : str
        name of country

    Returns
    -------
    str
        region name
    """
    return lkp.find_and_return_max("name", country, "region")
