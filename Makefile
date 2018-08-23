BINARY=gcpmetrics

VERSION=`cat VERSION`
BUILD=`git rev-parse HEAD`

LDFLAGS=-ldflags "-X main.Version=${VERSION} -X main.Build=${BUILD}"

.DEFAULT_GOAL: ${BINARY}

${BINARY}:
	go build -v ${LDFLAGS} -o ${BINARY} .

get:
	go get -v .

install:
	go install ${LDFLAGS} -o ${BINARY} .

clean:
	if [ -f ${BINARY} ] ; then rm -f ${BINARY} ; fi

.PHONY: clean install

