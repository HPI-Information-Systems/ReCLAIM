# Components
Components are reusable and self-contained building blocks. The following sections describe our groups of components.

## entityDetails
A detail page is a page about one specific entity, e.g., a 'Fruit-Stillife' (which is a cultural asset) or 'Renoir' (which is a person). This folder contains some components that help render these pages. Currently, three entity types have detail pages: cultural assets, persons and collections. There are specialized subdirectories for each of these entity types and a `general` directory containing components that can be used regardless of the specific entity type. 

### general
`comparisonTable.tsx` creates a table that compares an entity to similar entities in a table format.

`csvExport.tsx` is used to export a comparison table or information about a single entity in CSV format.

`detail.tsx` creates and structures the box on a detail page containing information about the entity itself.

`displayName.tsx` collects rules for all entity types, which information should be displayed as their title. It prioritizes different attributes for this.

`information.tsx` gets called by `detail.tsx` for each row of information. It distinguishes between relations and attributes to retrieve the information ('parsed') and adds information about the original value of the data ('raw').

`leadingInformation.tsx` renders information that should be displayed for each entity. These are their display name and their source.

`properties.tsx` retrieves the properties for a particular entity type located in their subdirectories. Properties refer to the selection of properties displayed as information about an entity on the entity's detail page. The particular `properties.tsx` files for each entity type also define the display order and name for the property labels.

`similarResults.tsx` shows entities that might describe the same entity. Checkboxes display information about a particular entity in the comparison table.

`types.tsx` defines enum types that are commonly used in multiple files.

### culturalAsset
Currently, only cultural assets have images, which is why components for displaying images are located here. We can display multiple images in a carousel using `imageCarousel`. `imageToolRow` adds image numbers to it (e.g., Image 2/5) and enables zoom functionality.

The subdirectory `provenanceTimeline` contains components that help display the provenance of a cultural asset in a timeline.

### person
`relatedEntities.tsx` displays what cultural assets a person owned or created and what collections they owned.

## general
This directory contains components to build the footer and header for the website.

It also collects all tooltip functions in `tooltip.tsx`. Tooltips show information when hovering over a certain area. They are used, e.g., to display original data when hovering over prepared data or to explain different types of buttons.

## search
This directory contains elements for the search box and for the search results. 

The search box gets put together with `searchBox.tsx`. It contains a basic search (`fulltextSearch.tsx`) and an advanced search (`advancedSearch.tsx`), where the query for each row is matched to a selected keyword (`keywordSelect.tsx`). To switch between the basic and advanced mode, `searchSwitch.tsx` is used. 

The `searchResults` subdirectory contains components for the search results. `resultBox` displayes all search results. As we only display a fixed number of results on each page (20), it uses a paginator (`resultsPaginator.tsx`) to navigate between the pages of results. `resultPreview.tsx` shows the results in little boxes that contain the most important information on the entity, like their title, their source, and an image (if no images exist, known identifiers are shown). 

## ui
The elements in this folder were taken from https://ui.shadcn.com/, which is an open source library of accessible and customizable components for web apps.

Some of the components in this folder are customized, to better fit the style of the platform.
