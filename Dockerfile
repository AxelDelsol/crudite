FROM golang:1.22

WORKDIR /app

COPY go.mod ./
COPY cmd/ ./cmd/
COPY internal/ ./internal/

RUN go build -o sample-api cmd/api-server/main.go

EXPOSE 8080

CMD [ "./sample-api" ]