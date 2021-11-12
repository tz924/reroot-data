# init.R
# Used to install required packages

my_packages = c(
  "plumber", 
  "dplyr",
  "tidyr",
  "future",
  "tidycensus"
)


# Install packages not yet installed
install_if_missing = function(p) {
  if (p %in% rownames(installed.packages()) == FALSE) {
    install.packages(p, dependencies = TRUE)
  }
}

# Packaging loading
invisible(sapply(my_packages, install_if_missing))