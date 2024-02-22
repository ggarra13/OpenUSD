pxr_python_bin(usdotio
    DEPENDENCIES
        usd
)

if(UNIX)
    _get_install_dir(bin installDir)
    
    install(
	FILES set_usdotio_env.sh
	DESTINATION ${installDir}
    )
endif()

# \todo: add tests
