my_data_3 <- read.csv("listings_cleaned.csv")
my_data_2 <- read.csv("good_reviews.csv")
library(dplyr)

good_listings <- my_data_3 |>
  mutate(id = as.character(id)) |>
  inner_join(
    my_data_2 |>
      transmute(
        listing_id = as.character(listing_id)
      ),
    by = c("id" = "listing_id")
  )
good_property_types <- good_listings |>
  group_by(
    neighbourhood_cleansed,
    property_type,
    bedrooms_clean
  ) |>
  summarize(
    number_of_good_reviews = n(),
    unique_properties = n_distinct(id),
    .groups = "drop"
  ) |>
  arrange(desc(number_of_good_reviews))

View(good_property_types)
write.csv(
  good_property_types,
  "good_property_types_bedrooms.csv",
  row.names = FALSE
)