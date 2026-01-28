# Use the official Golang image to create a build artifact.
# This is the "builder" stage.
FROM golang:1.25-alpine as builder
# checkov:skip=CKV_DOCKER_2: "Healthcheck not required for this build stage/app"
# checkov:skip=CKV_DOCKER_3: "Root user required for this specific container"

# Set the Current Working Directory inside the container
WORKDIR /app

# Copy go mod and sum files
COPY go.mod go.sum ./

# Download all dependencies. Dependencies will be cached if the go.mod and go.sum files are not changed
RUN go mod download

# Copy the source code
COPY . .

# Build the Go app
# -o gke-mcp: output file name
# -ldflags="-w -s": link with flags to reduce binary size
RUN CGO_ENABLED=0 GOOS=linux go build -a -ldflags="-w -s" -o gke-mcp .

# Start a new stage from scratch for a smaller image
FROM alpine:latest
# checkov:skip=CKV_DOCKER_7: "Using latest alpine is intentional for this base"

WORKDIR /root/

# Copy the Pre-built binary file from the previous stage
COPY --from=builder /app/gke-mcp .

# Expose port 8080 to the outside world
EXPOSE 8080

# Command to run the executable
CMD ["./gke-mcp", "--server-mode", "http", "--server-host", "0.0.0.0", "--server-port", "8080", "--allowed-origins", "*"]
