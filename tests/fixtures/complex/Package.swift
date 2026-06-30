// swift-tools-version:5.9
import PackageDescription

let package = Package(
    name: "ComplexFixture",
    dependencies: [
        .package(url: "https://github.com/vapor/vapor", from: "4.89.0"),
        .package(url: "https://github.com/apple/swift-argument-parser", exact: "1.3.0"),
        .package(url: "https://github.com/apple/swift-nio.git", .upToNextMajor(from: "2.65.0")),
    ]
)
