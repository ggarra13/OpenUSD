

install(
    FILES
    generatedSchema.usda
    plugInfo.json
    schema.usda
    
    DESTINATION ${CMAKE_INSTALL_PREFIX}/share/usd/examples/plugin/usdOtio
    )
