# Pure financial helpers. The Rmd embeds this exact code so it is self-contained.
# days = return-commute days in a 30-day month; commuters = household workers.
transit_cost <- function(days, commuters, boardings, fare, pass_price) {
  per_person <- pmin(2 * days * boardings * fare, pass_price)
  commuters * per_person
}

# The per-km amount is an assumed incremental operating rate, not ownership cost.
car_cost <- function(round_trip_km, days, commuters, per_km, parking) {
  commuters * (round_trip_km * days * per_km + ifelse(days > 0, parking, 0))
}

# Input minutes already contains BOTH directions; do not multiply by two again.
monthly_hours <- function(round_trip_minutes, days, commuters) {
  round_trip_minutes * days * commuters / 60
}

generalized_cost <- function(rent, utilities, transport, hours, time_value) {
  rent + utilities + transport + hours * time_value
}

# A positive threshold exists here only when the noncentral option is cheaper
# directly but consumes more commuting time. Other cases require separate labels.
break_even_value <- function(direct_difference, extra_hours) {
  ifelse(direct_difference < 0 & extra_hours > 0,
         -direct_difference / extra_hours, NA_real_)
}
