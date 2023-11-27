# Install and load required packages
if (!require("shiny")) install.packages("shiny")
if (!require("DiagrammeR")) install.packages("DiagrammeR")

library(shiny)
library(DiagrammeR)

# Define UI
ui <- fluidPage(
  titlePanel("Astronomical Research Library API Diagram"),
  mainPanel(
    grVizOutput("apiDiagram")
  )
)

# Define server
server <- function(input, output) {
  
  # Create the API diagram
  output$apiDiagram <- renderGrViz({
    # Define the graph using DiagrammeR syntax
    apiGraph <- "
      digraph api {
        # Nodes
        node [shape = box, style = filled, fillcolor = lightblue]
        DataPreprocessing [label = \"Data Preprocessing\"]
        MetadataExtractor [label = \"Metadata Extraction\"]
        WavelengthAlignment [label = \"Wavelength Alignment\"]
        SpectralVisualizer [label = \"Spectral Visualizer\"]
        DataAugmentation [label = \"Data Augmentation\"]
        AstronomicalClassifier [label = \"Astronomical Classifier\"]
        FeatureExtractor [label = \"Feature Extractor\"]
        
        # Additional Feature 1 (Machine Learning)
        AstronomicalClassifier -> {fit predict predict_proba}
        
        # Additional Feature 2 (Spectral Feature Extraction)
        FeatureExtractor -> extract_spectral_features
        
        # Connections
        DataPreprocessing -> {load_data normalize remove_outliers interpolate correct_redshift}
        MetadataExtractor -> extract_metadata
        WavelengthAlignment -> align_wavelength
        SpectralVisualizer -> visualize_spectrum
        DataAugmentation -> augment_data
      }
    "
    
    # Render the graph
    grViz(apiGraph)
  })
}

# Run the application
shinyApp(ui = ui, server = server)
