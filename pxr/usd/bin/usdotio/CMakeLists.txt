set(PXR_PREFIX pxr/usd)
set(PXR_PACKAGE usd)

pxr_python_bin(usdotio
    DEPENDENCIES
    usd
    tf
    sdf
)


pxr_install_test_dir(
    SRC testenv/testUsdOtioAdd
    DEST testUsdOtioAdd1
)

pxr_register_test(testUsdOtioAdd1
    PYTHON
    COMMAND "${CMAKE_INSTALL_PREFIX}/bin/usdotio add -o out.usda a.otio a.usda"
    DIFF_COMPARE out.usda
    EXPECTED_RETURN_CODE 0
    PRE_PATH
        ${CMAKE_INSTALL_PREFIX}/bin
)
