my_data_1 <- read.csv("listings_cleaned.csv")
my_data <- read.csv("reviews.csv")
View(my_data_1)
names(my_data_1)
names(my_data)
library(dplyr)
library(stringr)

reviews_summary <- my_data |>
  mutate(listing_id = as.character(listing_id)) |>
  group_by(listing_id) |>
  summarize(
    total_written_reviews = n(),
    .groups = "drop"
  )
combined_data <- my_data_1 |>
  mutate(id = as.character(id)) |>
  left_join(
    reviews_summary,
    by = c("id" = "listing_id")
  ) |>
  mutate(
    total_written_reviews = coalesce(total_written_reviews, 0L)
  )

neighbourhood_reviews <- combined_data |>
  group_by(neighbourhood = neighbourhood_cleansed) |>
  summarize(
    active_properties = n(),
    
    avg_rating =
      round(mean(review_scores_rating, na.rm = TRUE), 2),
    
    avg_value_rating =
      round(mean(review_scores_value, na.rm = TRUE), 2),
    
    avg_number_of_reviews =
      round(mean(number_of_reviews, na.rm = TRUE), 1),
    
    avg_written_reviews =
      round(mean(total_written_reviews, na.rm = TRUE), 1),
    
    .groups = "drop"
  ) |>
  arrange(desc(avg_rating))

print(neighbourhood_reviews, n = 25)

View(combined_data)
write.csv(combined_data, "combined_data.csv", row.names = FALSE)