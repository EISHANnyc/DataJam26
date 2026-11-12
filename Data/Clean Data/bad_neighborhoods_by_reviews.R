my_data_3 <- read.csv("listings_cleaned.csv")
my_data_4 <- read.csv("bad_reviews.csv")
View(my_data_3)
names(my_data_3)
names(my_data_2)
library(dplyr)
library(stringr)
bad_listings <- my_data_3 |>
  mutate(id = as.character(id)) |>
  inner_join(
    my_data_4 |>
      rename(review_id = id) |>
      mutate(listing_id = as.character(listing_id)),
    by = c("id" = "listing_id")
  )

bad_neighbourhood_properties <- bad_listings |>
  group_by(neighbourhood_cleansed) |>
  summarize(
    number_of_bad_reviews = n(),
    unique_properties = n_distinct(id),
    .groups = "drop"
  ) |>
  arrange(desc(number_of_bad_reviews))

View(bad_neighbourhood_properties)