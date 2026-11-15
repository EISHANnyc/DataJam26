my_data_3 <- read.csv("listings_cleaned.csv")
my_data_4 <- read.csv("bad_reviews.csv")
library(dplyr)
bad_listings <- my_data_3 |>
  mutate(id = as.character(id)) |>
  inner_join(
    my_data_4 |>
      transmute(
        listing_id = as.character(listing_id)
      ),
    by = c("id" = "listing_id")
  )
bad_property_types <- bad_listings |>
  group_by(
    neighbourhood_cleansed,
    property_type,
    bedrooms_clean
  ) |>
  summarize(
    number_of_bad_reviews = n(),
    unique_properties = n_distinct(id),
    .groups = "drop"
  ) |>
  arrange(desc(number_of_bad_reviews))

View(bad_property_types)
write.csv(
  bad_property_types,
  "bad_property_types_bedrooms.csv",
  row.names = FALSE
)