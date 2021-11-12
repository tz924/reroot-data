FROM virtualstaticvoid/heroku-docker-r:plumber
ENV PORT=8080
CMD ["/usr/bin/R", "--no-save", "--gui-none", "-f", "/app/app.R"]