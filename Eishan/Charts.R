library(tidyverse)
library(scales)

theme_dark_square <- theme_minimal(base_size = 12) +
  theme(
    plot.background   = element_rect(fill = "#1E1E1E", color = NA),
    panel.background  = element_rect(fill = "#1E1E1E", color = NA),
    panel.grid.major  = element_line(color = "#333333"),
    panel.grid.minor  = element_blank(),
    text              = element_text(color = "#FFFFFF"),
    axis.text         = element_text(color = "#E5E7EB", size = 10),
    axis.title        = element_text(color = "#FFFFFF", face = "bold", size = 10.5),
    plot.title        = element_text(face = "bold", size = 13, color = "#FFFFFF"),
    plot.subtitle     = element_text(size = 9.5, color = "#9CA3AF", margin = margin(b = 8)),
    plot.caption      = element_text(size = 7.5, color = "#9CA3AF", hjust = 0),
    plot.margin       = margin(12, 12, 10, 12)
  )

# 1
p_yield <- tibble(
  type = factor(c("Condos\n($688k)", "Townhouses\n($1.03M)", "Houses\n($1.82M)"),
                levels = c("Condos\n($688k)", "Townhouses\n($1.03M)", "Houses\n($1.82M)")),
  yield = c(6.63, 4.97, 2.18)
) |>
  ggplot(aes(type, yield, fill = type)) +
  geom_col(width = 0.55, show.legend = FALSE) +
  geom_text(aes(label = paste0(yield, "%")), vjust = -0.5, color = "#FFFFFF", fontface = "bold", size = 4.2) +
  scale_y_continuous(limits = c(0, 8), labels = \(x) paste0(x, "%")) +
  scale_fill_manual(values = c("#2DD4BF", "#64748B", "#F87171")) +
  labs(title = "Condos Yield 3x More Than Houses",
       subtitle = "Annual Airbnb revenue / CREA June 2026 price",
       x = NULL, y = "Gross Rental Yield (%)",
       caption = "Data: Inside Airbnb (15 June 2026) & CREA MLS® HPI.") +
  theme_dark_square
ggsave("chart_yield_by_type.png", p_yield, width = 5, height = 5, dpi = 300)

# 2
df_frontier_totals <- tibble(
  mix = factor(
    c("0 Condos\n4 Houses", "3 Condos\n3 Houses", "6 Condos\n2 Houses", "9 Condos\n1 House", "13 Condos\n0 Houses"),
    levels = c("0 Condos\n4 Houses", "3 Condos\n3 Houses", "6 Condos\n2 Houses", "9 Condos\n1 House", "13 Condos\n0 Houses")
  ),
  total_rev = c(159132, 283651, 408170, 532689, 711889),
  risk      = c("25.0%", "16.7%", "12.5%", "10.0%", "7.7%")
)

df_frontier_stack <- tibble(
  mix = factor(
    rep(c("0 Condos\n4 Houses", "3 Condos\n3 Houses", "6 Condos\n2 Houses", "9 Condos\n1 House", "13 Condos\n0 Houses"), each = 2),
    levels = c("0 Condos\n4 Houses", "3 Condos\n3 Houses", "6 Condos\n2 Houses", "9 Condos\n1 House", "13 Condos\n0 Houses")
  ),
  asset_type = factor(rep(c("Condos", "Houses"), times = 5), levels = c("Condos", "Houses")),
  part_rev   = c(
    0,      159132,
    164302, 119349,
    328604,  79566,
    492906,  39783,
    711889,      0
  )
)

p_frontier <- ggplot() +
  geom_col(
    data = df_frontier_stack,
    aes(x = mix, y = part_rev, fill = asset_type),
    width = 0.58,
    show.legend = FALSE
  ) +
  geom_text(
    data = df_frontier_totals,
    aes(x = mix, y = total_rev, label = paste0("$", round(total_rev / 1000), "k\n(", risk, " risk)")),
    vjust = -0.25,
    color = "#FFFFFF",
    fontface = "bold",
    size = 3.2
  ) +
  scale_y_continuous(limits = c(0, 860000), labels = dollar_format()) +
  scale_fill_manual(values = c("Condos" = "#2DD4BF", "Houses" = "#F87171")) +
  labs(
    title    = "Only Condos Beat Every Other Mix",
    subtitle = "Teal = Condos, Red = Houses | Revenue & 1-unit vacancy risk",
    x = NULL, y = "Annual Gross Revenue (CAD)",
    caption  = "Data: Inside Airbnb (15 June 2026), CREA & CMHC."
  ) +
  theme_minimal(base_size = 12) +
  theme(
    plot.background       = element_rect(fill = "#1E1E1E", color = NA),
    panel.background      = element_rect(fill = "#1E1E1E", color = NA),
    panel.grid.major      = element_line(color = "#333333"),
    panel.grid.minor      = element_blank(),
    text                  = element_text(color = "#FFFFFF"),
    axis.text             = element_text(color = "#E5E7EB", size = 9.5),
    axis.title            = element_text(color = "#FFFFFF", face = "bold", size = 10),
    plot.title.position   = "plot",
    plot.caption.position = "plot",
    plot.title            = element_text(face = "bold", size = 12.5, color = "#FFFFFF"),
    plot.subtitle         = element_text(size = 9, color = "#9CA3AF", margin = margin(b = 8)),
    plot.caption          = element_text(size = 7.5, color = "#9CA3AF", hjust = 0),
    plot.margin           = margin(12, 12, 10, 12)
  )
ggsave("chart_strategy_tradeoff.png", p_frontier, width = 5, height = 5, dpi = 300)

# 3
df_where <- tibble(
  neighbourhood = c("Downtown", "Shaughnessy", "Oakridge", "Kitsilano", "Fairview", "Riley Park", "Mount Pleasant"),
  mean_revpar   = c(160, 146, 142, 133, 133, 121, 115),
  status        = factor(
    c("Target Pick", "Rejected (~20% Occ)", "Rejected (~20% Occ)", "Target Pick", "Other", "Other", "Other"),
    levels = c("Target Pick", "Rejected (~20% Occ)", "Other")
  )
)
p_where <- ggplot(df_where, aes(x = reorder(neighbourhood, mean_revpar), y = mean_revpar, fill = status)) +
  geom_col(width = 0.62) +
  geom_text(aes(label = paste0("$", mean_revpar)), hjust = -0.2, color = "#FFFFFF", fontface = "bold", size = 3.6) +
  coord_flip() +
  scale_y_continuous(limits = c(0, 205), labels = dollar_format()) +
  scale_fill_manual(values = c(
    "Target Pick"         = "#2DD4BF",
    "Rejected (~20% Occ)" = "#F87171",
    "Other"               = "#475569"
  )) +
  labs(
    title    = "Downtown & Kitsilano Lead Target RevPAR",
    subtitle = "Shaughnessy & Oakridge sit empty ~80% of the year",
    x = NULL, y = "Mean RevPAR (CAD / Night)",
    caption  = "Data: Inside Airbnb, Vancouver, 15 June 2026, CC BY 4.0."
  ) +
  theme_minimal(base_size = 11.5) +
  theme(
    plot.background       = element_rect(fill = "#1E1E1E", color = NA),
    panel.background      = element_rect(fill = "#1E1E1E", color = NA),
    panel.grid.major      = element_line(color = "#333333"),
    panel.grid.minor      = element_blank(),
    text                  = element_text(color = "#FFFFFF"),
    axis.text             = element_text(color = "#E5E7EB", size = 9.5),
    axis.title            = element_text(color = "#FFFFFF", face = "bold", size = 10),
    plot.title.position   = "plot",
    plot.caption.position = "plot",
    plot.title            = element_text(face = "bold", size = 13, color = "#FFFFFF"),
    plot.subtitle         = element_text(size = 9, color = "#9CA3AF", margin = margin(b = 4)),
    plot.caption          = element_text(size = 7.5, color = "#9CA3AF", hjust = 0),
    legend.position       = "top",
    legend.justification  = "left",
    legend.title          = element_blank(),
    legend.text           = element_text(size = 8.5, color = "#E5E7EB"),
    legend.key.size       = unit(0.4, "cm"),
    plot.margin           = margin(12, 14, 10, 10)
  )
ggsave("chart_where_revpar.png", p_where, width = 5, height = 5, dpi = 300)