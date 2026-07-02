module github.com/okfgen/workspace

go 1.21

require (
    github.com/okfgen/go-utils v0.0.0
    github.com/okfgen/go-service v0.0.0
)

replace (
    github.com/okfgen/go-utils => ../go/easy
    github.com/okfgen/go-service => ../go/complex
)
