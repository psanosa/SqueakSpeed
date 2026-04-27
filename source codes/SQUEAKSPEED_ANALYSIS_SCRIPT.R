# Install and load dplyr package
install.packages("dplyr")
library(dplyr)

# Read the CSV file
data <- read.csv("ADD EXISTING FILE NAME HERE") %>%
  rename(DateTime = created_at, RotSess = field1, SessDist = field2,
         AvgSpeed = field3, AvgAcc = field4) %>%
  select(-entry_id, -latitude, -longitude, -elevation, -status)

# Convert the time stamps to POSIXct
data$DateTime <- as.POSIXct(data$DateTime, format = "%Y-%m-%dT%H:%M:%S")

# Create intervals of 59 minutes
interval_length <- 59 * 60

# Calculate average and standard error for each interval
result <- data %>%
  mutate(interval_group = floor(as.numeric(DateTime) / interval_length)) %>%
  group_by(interval_group) %>%
  summarise(
    count = n(),
    average_value = mean(INPUT PARAMETER HERE),
    sum_value = sum(INPUT PARAMETER HERE),
    standard_deviation = sd(INPUT PARAMETER HERE),
    standard_error = sd(INPUT PARAMETER HERE) / sqrt(n())
  ) %>%
  ungroup()

# Export data to csv file
write.csv(result, file = "ADD NEW FILE NAME HERE")

# Reset
rm(data, result, interval_length)
