# Ruby application entry point.

class App
  attr_reader :name, :version

  # Initialize the application.
  # @param name [String] application name
  # @param version [String] semver version string
  def initialize(name, version = "0.1.0")
    @name = name
    @version = version
    @routes = []
  end

  # Register a new route.
  # @param path [String] URL path
  # @param handler [Proc] route handler
  def get(path, &handler)
    @routes << { path: path, handler: handler }
  end

  # Return application info as a hash.
  def info
    { name: @name, version: @version, routes: @routes.length }
  end
end
