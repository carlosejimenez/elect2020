# We are using 2020 presidential election data at state level
# our prediction at state level comes from 538 prediction output
# Battle ground state should be identified using 2016 data

library(tidyverse)
pred_data_538 <- read_csv("../538_data/presidential_state_toplines_2020.csv")
result_2016 <- read_csv("../label_data/2016_pres_labels_battleground.csv")
result_2020 <- read_csv("../label_data/2020_pres_labels_battleground.csv")
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

# step 3: include battleground states marker from 2020 prez with 2016
battleground_marker_2016 <- result_2016 %>%
  select(state, battleground) %>%
  rename(battleground_2016 = battleground)

result_2020 <- result_2020 %>%
  rename(battleground_2020 = battleground) %>% 
  left_join(battleground_marker_2016)

data_w_2020_results <- subset %>%
  dplyr::left_join(result_2020) %>%
  dplyr::mutate(rep_vote_share_pred = rep_vote_share_pred/100, 
                dem_vote_share_pred = dem_vote_share_pred/100) %>%
  dplyr::rename(dem_vote_share_act_2020 = dem_vote_share, 
                rep_vote_share_act_2020 = rep_vote_share) %>%
  dplyr::mutate(mae_2020 = abs(rep_vote_share_pred - rep_vote_share_act_2020), 
                error_2020 = rep_vote_share_pred - rep_vote_share_act_2020)

days <- lubridate::ymd(c("2020-06-01", "2020-07-01","2020-08-01","2020-09-01", "2020-10-01", "2020-10-29"))

monthly_state <-  data_w_2020_results %>% filter(modeldate %in% days)

ggplot(monthly_state, aes(factor(modeldate), mae_2020, color = battleground_2016)) +
  geom_jitter(width = 0.1)+
  ggtitle("Mean Absolute Error of 538 Prediction")+
  ggsave()

monthly_mae_sumstats <- monthly_state %>%
  group_by(modeldate, battleground_2016) %>%
  summarize(mean_MAE = mean(mae_2020), 
            sd_MAE = sd(mae_2020), 
            se_MAE=sd_MAE/sqrt(n()),
            median_MAE = median(mae_2020),
            n_states = n(), 
            upper_95 = mean_MAE + qnorm(0.975)*se_MAE, 
            lower_95 = mean_MAE - qnorm(0.975)*se_MAE) 

ggplot(monthly_mae_sumstats, aes(modeldate, mean_MAE, color = battleground_2016)) +
  geom_line(aes(group = battleground_2016))+
  geom_errorbar(aes(ymin = lower_95, ymax = upper_95), position = "dodge", width = 5)


ggplot(monthly_state, aes(factor(modeldate), error_2020, color = battleground_2016)) +
  geom_jitter(width = 0.1)+
  ggtitle("Prediction Error in Vote Share Based on 538 Prediction")+
  xlab("Prediction Date")
