library(dplyr)
library(tidyr)
library(rstatix)

add_stars <- function(df) {
    # Add a new column with significance stars
    df <- df %>%
    mutate(adj.p.signif = case_when(
        adj.p.value <= 0.001 ~ "***",
        adj.p.value <= 0.01 ~ "**",
        adj.p.value <= 0.05 ~ "*",
        adj.p.value <= 0.1 ~ ".",
        TRUE ~ ""
    ))
    return(df)
}

preprocess <- function(df) {
    head(df)
    keys_to_drop <- c("timestamp")

    # drop the extra metadata
    df <- df %>% select(-c(keys_to_drop))

    df$solved[df$solved == "True"] <- 1
    df$solved[df$solved == "False"] <- 0
    df$solved <- as.numeric(df$solved)

    # drop na values -> sometimes a move might have no eval data if made quickly
    df <- df %>% na.omit()
    df <- df %>% filter(pid != "")

    return(df)
}

remove_outliers <- function(df) {
    df$unique_id <- paste(df$pid, df$block_id, sep = "_")

    all_outlier_uids <- c()
    for (p in unique(df$pid)) {
        pdf <- df %>% filter(pid == p)
        outliers <- sapply(colnames(pdf), function(col) {
            if (col %in% c("elo", "elo_bin", "solved", "pid", "unique_id", "block_id")) return(FALSE)        #nolint
            pdf %>% select(col) %>% identify_outliers() %>% filter(is.extreme == TRUE)                       #nolint
        })
        # remove all puzzles that contain extreme outliers from the braindata.
        outlier_unique_ids <- sapply(outliers, function(outlier_df) {
            tryCatch(
                return(unique(outlier_df$unique_id)),
                error = function(e) {  # What to do when an error occurs
                    return(c())
                }
            )
        })
        all_outlier_uids <- c(all_outlier_uids, outlier_unique_ids)
    }

    flat_outlier_unique_ids <- unique(unlist(all_outlier_uids))

    df <- df %>% filter(!(unique_id %in% flat_outlier_unique_ids))
    return(df)
}

make_long <- function(df) {
    return(df %>%
        gather(variable, value, -pid, -solved, -block_id, -unique_id, -elo, -elo_bin) %>%
        separate(variable, c("wavelength", "probe"), sep = "\\.", extra = "merge")
    )
}

# label the data with 0/1 depending on whether the game was lo/hi elo for the given participant. 
label_data <- function(df) {
    sumry <- df %>% group_by(pid) %>% summarize(lower = quantile(elo, 0.25),
                                                upper = quantile(elo, 0.75))
    # for each pid, i'd like to mark each puzzle as 0, 1, or 2, where 0 is any puzzle
    # less than or equal to the 25th percentile, 1 is between the 25th and 75th percentile,
    # and 2 is greater than or equal to the 75th percentile.

    # Join the 'df' and 'sumry' data frames
    df_with_sumry <- df %>% left_join(sumry, by = "pid")

    # Create a new column based on the elo values and the quartiles
    df_with_new_col <- df_with_sumry %>% mutate(
        elo_category = case_when(
            elo <= lower ~ 0,
            elo > lower & elo < upper ~ 2,
            elo >= upper ~ 1
        )
    )

    df$evaluation <- df_with_new_col$elo_category

    df <- df %>% select(-c(elo)) # unique_id

    return(df)
}

observe_elos <- function(df) {
    #get a sense of the data
    for (p in unique(df$pid)) {
        pdf <- df %>% filter(pid == p)
        elos <- pdf$elo
        print(p)
        print(summary(elos))
    }
}
