FROM golang:1.17.3

RUN git config --global http.sslverify false
COPY . /go/src/github.com/harlow/go-micro-services
WORKDIR /go/src/github.com/harlow/go-micro-services
RUN go get gopkg.in/mgo.v2
RUN go get github.com/bradfitz/gomemcache/memcache
RUN go get github.com/google/uuid
RUN go mod init
RUN go mod vendor

# use local modified packages instead of upstream one
COPY ./vendor/github.com/hailocab/go-geoindex /go/src/github.com/harlow/go-micro-services/vendor/github.com/hailocab/go-geoindex
COPY ./vendor/levelgzip /go/src/github.com/harlow/go-micro-services/vendor/levelgzip
COPY ./vendor/google.golang.org/grpc /go/src/github.com/harlow/go-micro-services/vendor/google.golang.org/grpc

# # plugin to golang src code
# COPY ./golang-plugin/malloc.go /usr/local/go/src/runtime/malloc.go
# COPY ./golang-plugin/sizeclasses.go /usr/local/go/src/runtime/sizeclasses.go

RUN go install -ldflags="" ./cmd/...
