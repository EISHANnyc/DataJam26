my_data <- read.csv("reviews.csv")
library(dplyr)
library(stringr)

library(dplyr); library(stringr)   # install.packages("stringr") if needed
english <- my_data %>%
  filter(!is.na(comments), detect_language(comments) %in% "en") %>%
  mutate(score = get_sentiment(comments, method = "bing"),
         sentiment = case_when(score > 0 ~ "good", score < 0 ~ "bad", TRUE ~ "neutral"))
text <- english$comments %>%
  str_to_lower() %>%
  str_replace_all("[\u2018\u2019]", "'")

# 1. Remove phrases that sound negative but are actually praise
praise <- c("not disappointed", "never disappointed", "won't be disappointed",
            "will not be disappointed", "wouldn't be disappointed",
            "no regrets", "not regret", "won't regret", "will not regret",
            "no complaints", "can't complain", "can't fault",
            "no issues", "no problems", "no problem")
text <- str_replace_all(text, str_c(praise, collapse = "|"), " ")

# 2. Count real complaint phrases (edit this list as you go)
complaints <- c("not recommend", "wouldn't recommend", "would not recommend",
                "don't recommend", "do not recommend", "avoid this", "avoid at all",
                "stay away", "don't stay", "do not stay", "never again",
                "not as described", "not as advertised", "misleading", "false advertising",
                "disappoint", "zero stars", "one star", "1 star",
                "dirty", "filthy", "unclean", "not clean", "cockroach", "bed bug", "bedbug",
                "mold", "mould", "musty", "smelly", "stinks", "rude", "unresponsive",
                "scam", "refund", "unsafe", "sketchy", "overpriced",
                "terrible", "horrible", "awful", "worst", "nightmare", "disgusting", "unacceptable")

english$n_complaints <- str_count(text, str_c(complaints, collapse = "|"))

english$sentiment <- case_when(english$n_complaints >= 2 ~ "bad",
                               english$n_complaints == 1 ~ "mixed",
                               TRUE                      ~ "good")

table(english$sentiment)
good_reviews  <- filter(english, sentiment == "good")
mixed_reviews <- filter(english, sentiment == "mixed")
bad_reviews   <- filter(english, sentiment == "bad")
View(good_reviews)
View(bad_reviews)