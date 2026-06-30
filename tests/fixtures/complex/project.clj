(defproject complex-fixture "0.1.0"
  :description "A comprehensive test fixture"
  :dependencies [[org.clojure/clojure "1.11.1"]
                 [ring/ring-core "1.12.0"]
                 [compojure "1.7.0"]]
  :profiles {:dev {:dependencies [[cider/cider-nrepl "0.28.5"]]}})
