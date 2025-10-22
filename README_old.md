![cover](/@yamauchi_1980%20cover.png)

# Ag Dedicated

**TL;DR:**<br> 
Hawai‘i’s agricultural dedications provide tax incentives for both active farming and vacant agricultural land, with this project analyzing dedication data, tax benefits, and compliance using tools like mapping and imagery analysis.

## Overview
Tax incentives are widely used across the U.S. to support the agricultural sector and encourage the preservation of farmland. Differential assessments, also known as agricultural dedications, allow land to be taxed based on its agricultural use value rather than its often higher fair market value.

Agricultural dedications are a key tool, applied by every county in Hawai‘i, to help farmers reduce their property tax burden and keep agricultural land in production. This project compiles and reviews data relevant to this approach. [^1]


Learn more about [differential assessments](http://www.farmlandinfo.org/differential-assessment-and-circuit-breaker-tax-programs)  and other tax policies help protect farmland and support agriculture, visit the [Farmland Information Center](http://www.farmlandinfo.org) of the [American Farmland Trust](https://www.farmland.org).

## State of Hawaii

First establish in Maryland in 1957, then in Hawaii in 1963

[Hawaii Revised Statutes §246-12](https://law.justia.com/codes/hawaii/2013/title-14/chapter-246/section-246-12) outlines statewide rules for


## Honolulu County
In Hawaii, each county provides some form of differential assessment for agricultural use. On Oahu, the [Revised Ordinances of Honolulu §8-7.3](https://codelibrary.amlegal.com/codes/honolulu/latest/honolulu/0-0-0-5936) outlines the process and regulations for dedicating agricultural land. The ordinance provides a framework for landowners to commit their property to agricultural use for specific periods, offering tax benefits in return for maintaining the land's agricultural use. Each year there are around 1400 agricultural dedications across the island of Oahu. 


The ordinance covers several important aspects:
- Dedication Periods: Landowners can dedicate their land for 5 or 10 years for specific agricultural uses, or 10 years as vacant agricultural land.
- Tax Assessment: Dedicated lands receive preferential tax treatment, with 5-year dedications assessed at 3% of fair market value and 10-year dedications at 1%.
- Obligations: Owners must maintain substantial and continuous agricultural use, defined as at least 75% of usable land in active, revenue-generating agricultural production.
- Petition Process: Landowners must file a petition with the director, including an agricultural plan detailing the proposed use.
- Annual Reporting: Dedicated land owners are required to submit annual reports on the agricultural use of the property.
- Cancellation and Penalties: The ordinance specifies conditions for cancellation of dedication and potential rollback taxes and penalties for non-compliance.

Dedicated areas (which are not to include the footprint of any residential homesite) "shall remain in substantial and continuous agricultural use." 
With "agricultural use of land" defined as the "active use of the land for the production of agricultural products." to "include such products as floricultural, horticultural, viticultural, aquacultural, forestry, nut, coffee, dairy, livestock, poultry, bee, animal, tree farm, animals raised by grazing and pasturing, and any other farm, agronomic, or plantation products."

## Project Approaches

**_1. Compile historical agricultural dedication data._**<br>
For the past decade, annual data releases from the Real Property Assessment Division haven been downloaded.

**_2. Collect tax data of currently dedicated parcels_**<br>
Previously this project aimed to relate (via scraping) public tax record data of currently dedicated parcels. Fortunately this data is now largely [readily available](https://prod-histategis.opendata.arcgis.com/datasets/cchnl::ownerdat-table/about).

**_3. Map existing dedications and assess their distribution_**<br>
Earlier approaches were trickier as readily public property ownership data was minimal. 

https://honolulu-cchnl.opendata.arcgis.com/datasets/cchnl::parcels-tax/about

**_4. Quantify total tax incentive provided by Honolulu County of Honolulu_**<br> 
The history of gross tax earnings and savings provide [some data](https://realproperty.honolulu.gov/state-reports/2024/)

**_5. Explore means to assess "substantial and continuous agricultural use"_**<br>
Automated imagery analysis processing as a possibility.

## References & Resources

Co, Howard, "History and Provisions of the Agricultural Dedication Law in Hawaii, August 1974, unpublished draft manuscript cited with permission of author.

Okimoto, Glenn Michiaki, 1981 OPTIMAL CONTROL FOR LAND USE DECISIONS IN HAWAII MODEL FORMULATION AND POTENTIAL APPLICABILITY

https://scholarspace.manoa.hawaii.edu/server/api/core/bitstreams/24ccafa9-0cf2-4ea8-a4e7-32f37c427f80/content

[1] 

[^1] sfsdf