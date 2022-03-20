# VetaQL Video Metadata Store 
A Video Metadata Store for Efficient Query and Retrieval

The VetaQL metadata store provides a highly efficient and optimized metadata store specifically tailored for video analytics and other video-related video metadata. 

## What does it do ?

VetaQL video metadata store tries to solve the problems posed with conventional methods of storing video metadata using an event model based approach. This metadata store also uses a SQL-like language called VetaQL to enable more complex and natural queries which are not possible by using conventional databases.

## When is VetaQL useful ?

Current database solutions cannot support the types of queries required for videos. Some real-world examples of queries that our project aims to solve are “Play clips of kids playing in the sand” or “which clips have a Boeing 747 land'' .These are just some of the real-world queries that can be run if the data is modelled as events rather than tables or documents. 

## VetaQL Language Query and Syntax
The query language for the video metadata store is heavily derived from SQL syntax and uses additional English language keywords to support more complex queries.

The general structure of any query irrespective of the type of events is as follows:
```
SELECT <event/experience>
...other event parameters...
FROM <domain_model>
```

The two important aspects(keywords) to note in the general structure of the query are:

```
SELECT <event/experience>
```

The event/experience is the actual experience captured by a section of the video.
This mandatory keyword is used to actually select or choose the event or experience from the database. It represents the objective of the query i.e to get events(think of events as the videos/clips ) from the database matching the query information to the metadata in the database using the event model.

```
FROM <domain_model>
```

The domain model represents the structure(database in MongoDB terms) of the domain that is being represented by the video. Each database represents a specific domain model, which is being referred to here. 

Using this general structure, other event parameters(types such as spatial, temporal, etc.) can be defined. Each has been dealt with separately as follows:

### Temporal: 

Temporal refers to the time period represented by the event or sub-event. To represent temporal events in the query, use the DURING keyword to represent the time period.
On top of DURING, the following keywords add more context to the keyword:
END OF - Representing the end of the time period specified.
BEGIN OF - Representing the beginning of the time period specified.
	Not mentioning the above indicates the query refers to that specific time period only.

Syntax:

```
SELECT <event/experience>
DURING END OF/BEGIN OF <time period>
FROM <domain_model>
```

Another important point to note about the temporal field is that it need not always refer to the time period in the temporal domain only, it can also refer to a domain-specific event within the domain model which happens during a specific time. For example consider sports Soccer(European),” half time” is a specific event with the domain model, but it also refers to the time period(temporal domain) during a match. 

### Spatial:

Spatial is used to represent spatial coordination or geolocations associated with sections of the video. In general, it represents the spatial locations we are trying to refer to in the query. To refer to spatial locations use the AT keyword.

Syntax:

```
SELECT <event/experience>
AT/IN/NEAR/ON <spatial location>
FROM <domain_model>
```

Apart from the AT keyword, to make the query more linguistic and representative, few alternative keywords may also be used which have the exact same syntactic meaning.
The keywords being: IN / NEAR / ON


### Informational: 

Informational aspects of a video domain model include people who were involved in the event and their attributes, roles. In some cases, informational data can even refer to objects in that event. To specify informational aspects, use the BY or HAVING TAG keyword(s).

Syntax:

```
SELECT <event/experience>
BY/HAVING TAG <person/object/role>
FROM <domain_model>
```

### Causality:

Causality represents how some events are caused by other events. When we are trying to represent causality in a query we could mean that the event either causes or is caused by another event(s). To facilitate this aspect in the query the following keywords can be used:
CAUSING - Indicates the event mentioned in the query causes another event.
CAUSED BY - Indicates the event mentioned in the query is caused by another event.

Syntax:

```
SELECT <event/experience>
CAUSING/CAUSED BY <event>
FROM <domain_model>
```

## Example

Consider the query:
```
“ Virat Kohli hitting a match-winning six at the end of the second innings at Adelaide“
```
For the above query, the following are the event aspects/properties:
- Event/Experience: hitting a six
- Domain model: cricket videos(it could also refer to India vs Australia database, this again depends on how the user has stored the model in the database)
- Temporal: end of the second innings
- Spatial: Adelaide
- Informational: Virat Kohli
- Causality: winning the match.

The structured query for the above example could then be of the form:

```
SELECT “hitting six”
DURING END OF “second innings”
AT “Adelaide”
BY “Virat Kohli”
CAUSING “match win”
FROM “India Australia cricket”
```

