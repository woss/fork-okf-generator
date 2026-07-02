# Domain model for generated reports.
module Models
  class Report
    attr_reader :id, :title, :generated_at
    attr_accessor :data

    def initialize(id, title, data = {})
      @id = id
      @title = title
      @data = data
      @generated_at = Time.now.utc
    end

    def to_h
      {
        id: @id,
        title: @title,
        data: @data,
        generated_at: @generated_at.iso8601
      }
    end

    def summary
      "#{@title} (#{@data.length} entries)"
    end
  end

  # A report that can be exported to CSV format.
  module Exportable
    def to_csv
      @data.map { |row| row.values.join(",") }.join("\n")
    end

    def to_json
      require "json"
      to_h.to_json
    end
  end

  # A scheduled report that runs at a specific interval.
  class ScheduledReport < Report
    include Exportable

    attr_reader :schedule, :last_run

    def initialize(id, title, schedule, data = {})
      super(id, title, data)
      @schedule = schedule
      @last_run = nil
    end

    def mark_as_run!
      @last_run = Time.now.utc
    end

    def due?
      return true if @last_run.nil?
      interval_seconds = case @schedule
                         when "daily" then 86_400
                         when "hourly" then 3_600
                         else 0
                         end
      (Time.now.utc - @last_run) >= interval_seconds
    end
  end
end
