my_data_3 <- read.csv("listings_cleaned.csv")
my_data_2 <- read.csv("good_reviews.csv")
View(my_data_3)
names(my_data_3)
names(my_data_2)
library(dplyr)
library(stringr)

good_listings <- my_data_3 |>
  mutate(id = as.character(id)) |>
  inner_join(
    my_data_2 |>
      mutate(listing_id = as.character(listing_id)),
    by = c("id" = "listing_id")
  )

good_neighbourhood_properties <- good_listings |>
  group_by(neighbourhood_cleansed) |>
  summarize(
    number_of_good_reviews = n(),
    unique_properties = n_distinct(id),
    .groups = "drop"
  ) |>
  arrange(desc(number_of_good_reviews))

View(good_neighbourhood_properties)