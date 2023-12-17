# Install and load required packages
if (!require("shiny"))
  install.packages("shiny")
if (!require("DiagrammeR"))
  install.packages("DiagrammeR")
if (!require("rsvg"))
  install.packages("rsvg")
if (!require("DiagrammeRsvg"))
  install.packages("DiagrammeRsvg")

# Define the graph using DiagrammeR syntax
apiGraph <- "
      digraph api {
        graph [rankdir = LR]
        # Nodes
        node [shape = box, style = filled, fillcolor = lightblue]
        FeatureExtractor [label = \"Feature Extractor\"]
        AstronomicalClassifier [label = \"Astronomical Classifier\"]
        DataAugmentation [label = \"Data Augmentation\"]
        SpectralVisualizer [label = \"Spectral Visualizer\"]
        WavelengthAlignment [label = \"Wavelength Alignment\"]
        MetadataExtractor [label = \"Metadata Extraction\"]
        DataPreprocessing [label = \"Data Preprocessing\"]
        DataQuery [label = \"Data Query\"]
        
        # Connections
        DataQuery -> {load_data_sql load_data_file load_data_ids load_data_constraints}
        DataPreprocessing -> {load_data normalize remove_outliers interpolate correct_redshift}
        MetadataExtractor -> extract_metadata
        WavelengthAlignment -> align_wavelength
        SpectralVisualizer -> visualize_spectrum
        DataAugmentation -> {standard_derivative fractional_derivative augment_data}

        # Additional Feature 1 (Machine Learning)
        AstronomicalClassifier -> {prepare_data fit_model predict_class predict_proba}

        # Additional Feature 2 (Spectral Feature Extraction)
        FeatureExtractor -> extract_spectral_features
      }
    "
# Render the graph
grViz(apiGraph) %>% export_svg %>% charToRaw %>% rsvg_png("diagram.png")