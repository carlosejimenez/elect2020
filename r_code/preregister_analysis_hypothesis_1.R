# this script attempts to validate the following hypothesis
# hypothesis:
# since this is a preregistered data anlysis. we have not seen the election results from 2020
# we will use election restuls from 2016 as the "true" election results
# our prediction at state level comes from 538 prediction output

library(tidyverse)
pred_data_538 <- read_csv("../538_data/presidential_state_toplines_2020.csv")
result_2016 <- read_csv("../label_data/2016_pres_labels_battleground.csv")
# Step 1: select columsn we would need
# vote share from incumbant, challenger and others
# state
# date that model is for, date when the model is generated


# Step 2: exclude data at sub-state districts (ME and NE)
subset <- pred_data_538 %>% 
  dplyr::select(modeldate, state, voteshare_inc, voteshare_chal, voteshare_other, 
         voteshare_inc_hi, voteshare_inc_lo, 
         voteshare_chal_hi, voteshare_chal_lo, 
         voteshare_other_hi, voteshare_other_lo, 
         timestamp) %>%
  dplyr::filter(!state %in% c("ME-1", "ME-2", "NE-1", "NE-2", "NE-3")) %>%
  dplyr::mutate(modeldate = lubridate::mdy(modeldate)) %>%
  dplyr::rename(dem_vote_share_pred = voteshare_chal, 
                rep_vote_share_pred = voteshare_inc)

states <- c("Wyoming", "Wisconsin", "West Virginia", "Washington","Virginia","Vermont","Utah","Texas","Tennessee")
draw_sample <- subset %>% filter(state %in% states)
ggplot(draw_sample, aes(x=modeldate, y = voteshare_inc, colour = state))+
  geom_line()


# step 3: include result from 2016 prez as if it's true election result for 2020

data_w_2016_results <- subset %>%
  dplyr::left_join(result_2016) %>%
  dplyr::mutate(rep_vote_share_pred = rep_vote_share_pred/100, 
                dem_vote_share_pred = dem_vote_share_pred/100) %>%
  dplyr::rename(dem_vote_share_act_2016 = dem_vote_share, 
                rep_vote_share_act_2016 = rep_vote_share) %>%
  dplyr::mutate(mae_2016 = abs(rep_vote_share_pred - rep_vote_share_act_2016))

days <- lubridate::ymd(c("2020-06-01", "2020-07-01","2020-08-01","2020-09-01", "2020-10-01", "2020-10-29"))

monthly_state <-  data_w_2016_results %>% filter(modeldate %in% days)

ggplot(monthly_state, aes(factor(modeldate), mae_2016, color = battleground)) +
  geom_jitter()

monthly_mae_sumstats <- monthly_state %>%
  group_by(modeldate, battleground) %>%
  summarize(mean_MAE = mean(mae_2016), 
            var_MAE = var(mae_2016), 
            median_MAE = median(mae_2016)) 

  
ggplot(monthly_summary, aes(modeldate, mean_MAE, color = battleground)) +
  geom_line()

ggplot(monthly_mae_sumstats, aes(modeldate, median_MAE, color = battleground)) +
  geom_line()
