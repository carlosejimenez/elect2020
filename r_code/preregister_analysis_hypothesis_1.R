# this script attempts to validate the following hypothesis
# hypothesis:
# since this is a preregistered data anlysis. we have not seen the election results from 2020
# we will use election restuls from 2016 as the "true" election results
# our prediction at state level comes from 538 prediction output

library(tidyverse)
pred_data_538 <- read_csv("../538_data/presidential_state_toplines_2020.csv")

# Step 1: select columsn we would need
# vote share from incumbant, challenger and others
# state
# date that model is for, date when the model is generated


# Step 2: exclude data at sub-state districts (ME and NE)
subset <- pred_data_538 %>% 
  select(modeldate, state, voteshare_inc, voteshare_chal, voteshare_other, 
         voteshare_inc_hi, voteshare_inc_lo, 
         voteshare_chal_hi, voteshare_chal_lo, 
         voteshare_other_hi, voteshare_other_lo, 
         timestamp) %>%
  filter(!state %in% c("ME-1", "ME-2", "NE-1", "NE-2", "NE-3")) %>%
  mutate(modeldate = lubridate::mdy(modeldate))

states <- c("Wyoming", "Wisconsin", "West Virginia", "Washington","Virginia","Vermont","Utah","Texas","Tennessee")
draw_sample <- subset %>% filter(state %in% states)
ggplot(draw_sample, aes(x=modeldate, y = voteshare_inc, colour = state))+
  geom_line()

data_w_fake_results <- subset %>%
  mutate(result)
