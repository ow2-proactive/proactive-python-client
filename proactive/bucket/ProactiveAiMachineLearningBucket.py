from .ProactiveBucket import ProactiveBucket

class ProactiveAiMachineLearningBucket(ProactiveBucket):
    """
    Represents the proactive ai-machine-learning bucket
    """

    def __init__(self, gateway):
        super(ProactiveAiMachineLearningBucket, self).__init__(gateway, "ai-machine-learning")
        self.setUseDefaultForkEnv(True)
        self._default_fork_env_container_platform = "docker"
        self._default_fork_env_container_gpu_enabled = False
        self._default_fork_env_container_image = ""
    
    def setUseDefaultForkEnv(self, enable_default_fork_env):
        self._enable_default_fork_env = enable_default_fork_env
    
    def setDefaultForkEnvContainerPlatform(self, container_platform):
        self._default_fork_env_container_platform = container_platform
    
    def setDefaultForkEnvContainerGpuEnabled(self, container_gpu_enabled):
        self._default_fork_env_container_gpu_enabled = container_gpu_enabled
    
    def setDefaultForkEnvContainerImage(self, container_image):
        self._default_fork_env_container_image = container_image
    
    def isDefaultForkEnvEnabled(self):
        return self._enable_default_fork_env
    
    def _addDefaultTaskSettings(self, proactive_task, __task_enabled, __work_dir, __limit_output_view, __precious_result):
        proactive_task.addVariable("TASK_ENABLED", str(__task_enabled))
        proactive_task.addVariable("WORK_DIR", __work_dir)
        proactive_task.addVariable("LIMIT_OUTPUT_VIEW", str(__limit_output_view))
        proactive_task.setPreciousResult(__precious_result)
        if self.isDefaultForkEnvEnabled():
            self._setDefaultForkEnv(proactive_task)
    
    def _setDefaultForkEnv(self, proactive_task):
        proactive_task_fork_env = self._gateway.createForkEnvironment(language="groovy")
        proactive_task_fork_env.setImplementationFromURL(self._base_url + "/catalog/buckets/scripts/resources/fork_env_ai/raw")
        proactive_task.setForkEnvironment(proactive_task_fork_env)
        proactive_task.addVariable("CONTAINER_PLATFORM", self._default_fork_env_container_platform)
        proactive_task.addVariable("CONTAINER_GPU_ENABLED", str(self._default_fork_env_container_gpu_enabled))
        proactive_task.addVariable("CONTAINER_IMAGE", self._default_fork_env_container_image)

    def create_Load_Iris_Dataset_task(self, 
                                      import_from="PA:URL",
                                      file_path="https://s3.eu-west-2.amazonaws.com/activeeon-public/datasets/iris.csv",
                                      file_delimiter=",",
                                      label_column="species",
                                      __task_enabled=True,
                                      __work_dir=".",
                                      __limit_output_view=-1,
                                      __precious_result=True):
        """
        Create the Load_Iris_Dataset task
        Load and return the iris dataset classification
        :return: A Python ProactiveTask object
        """
        proactive_task = self._gateway.createPythonTask()
        proactive_task.setTaskName("Load_Iris_Dataset")
        proactive_task.addVariable("IMPORT_FROM", import_from)
        proactive_task.addVariable("FILE_PATH", file_path)
        proactive_task.addVariable("FILE_DELIMITER", file_delimiter)
        proactive_task.addVariable("LABEL_COLUMN", label_column)
        proactive_task.setTaskImplementationFromURL(self._base_url + "/catalog/buckets/ai-machine-learning/resources/Load_Iris_Dataset_Script/raw")
        proactive_task.addGenericInformation("task.icon", "/automation-dashboard/styles/patterns/img/wf-icons/load_dataset.png")
        proactive_task.addGenericInformation("task.documentation", "PAIO/PAIOUserGuide.html#_load_iris_dataset")
        self._addDefaultTaskSettings(proactive_task, __task_enabled, __work_dir, __limit_output_view, __precious_result)
        return proactive_task
    
    def create_Load_Boston_Dataset_task(self,
                                        __task_enabled=True,
                                        __work_dir=".",
                                        __limit_output_view=-1,
                                        __precious_result=True):
        """
        Create the Load_Boston_Dataset task
        Load and return the boston house-prices dataset for regression
        :return: A Python ProactiveTask object
        """
        proactive_task = self._gateway.createPythonTask()
        proactive_task.setTaskName("Load_Boston_Dataset")
        proactive_task.setTaskImplementationFromURL(self._base_url + "/catalog/buckets/ai-machine-learning/resources/Load_Boston_Dataset_Script/raw")
        proactive_task.addGenericInformation("task.icon", "/automation-dashboard/styles/patterns/img/wf-icons/load_dataset.png")
        proactive_task.addGenericInformation("task.documentation", "PAIO/PAIOUserGuide.html#_load_boston_dataset")
        self._addDefaultTaskSettings(proactive_task, __task_enabled, __work_dir, __limit_output_view, __precious_result)
        return proactive_task

    def create_Download_Model_task(self,
                                   __task_enabled=True,
                                   __work_dir=".",
                                   __limit_output_view=-1,
                                   __precious_result=True):
        """
        Create the Download_Model task
        :return: A Python ProactiveTask object
        """
        proactive_task = self._gateway.createPythonTask()
        proactive_task.setTaskName("Download_Model")
        proactive_task.setTaskImplementationFromURL(self._base_url + "/catalog/buckets/ai-machine-learning/resources/Download_Model_Script/raw")
        proactive_task.addGenericInformation("task.icon", "/automation-dashboard/styles/patterns/img/wf-icons/download_model.png")
        proactive_task.addGenericInformation("task.documentation", "PAIO/PAIOUserGuide.html#_download_model")
        self._addDefaultTaskSettings(proactive_task, __task_enabled, __work_dir, __limit_output_view, __precious_result)
        return proactive_task

    def create_Export_Data_task(self,
                                output_type="CSV",
                                __task_enabled=True,
                                __work_dir=".",
                                __limit_output_view=-1,
                                __precious_result=True):
        """
        Create the Export_Data task
        Export the data in a specified format (CSV, JSON, HTML, TABLEAU, S3)
        :return: A Python ProactiveTask object
        """
        proactive_task = self._gateway.createPythonTask()
        proactive_task.setTaskName("Export_Data")
        proactive_task.addVariable("OUTPUT_TYPE", output_type)
        proactive_task.setTaskImplementationFromURL(self._base_url + "/catalog/buckets/ai-machine-learning/resources/Export_Data_Script/raw")
        proactive_task.addGenericInformation("task.icon", "/automation-dashboard/styles/patterns/img/wf-icons/export_data.png")
        proactive_task.addGenericInformation("task.documentation", "PAIO/PAIOUserGuide.html#_export_data")
        self._addDefaultTaskSettings(proactive_task, __task_enabled, __work_dir, __limit_output_view, __precious_result)
        return proactive_task

    def create_Import_Data_task(self, 
                                import_from="PA:URL", 
                                file_path="https://s3.eu-west-2.amazonaws.com/activeeon-public/datasets/pima-indians-diabetes.csv",
                                file_delimiter=";", 
                                label_column="class", 
                                data_type_identification="False",
                                __task_enabled=True,
                                __work_dir=".",
                                __limit_output_view=-1,
                                __precious_result=True):
        """
        Create the Import_Data task
        Load data from external sources and detect its features type if requested
        :return: A Python ProactiveTask object
        """
        proactive_task = self._gateway.createPythonTask()
        proactive_task.setTaskName("Import_Data")
        proactive_task.addVariable("IMPORT_FROM", import_from)
        proactive_task.addVariable("FILE_PATH", file_path)
        proactive_task.addVariable("FILE_DELIMITER", file_delimiter)
        proactive_task.addVariable("LABEL_COLUMN", label_column)
        proactive_task.addVariable("DATA_TYPE_IDENTIFICATION", data_type_identification)
        proactive_task.setTaskImplementationFromURL(self._base_url + "/catalog/buckets/ai-machine-learning/resources/Import_Data_Script/raw")
        proactive_task.addGenericInformation("task.icon", "/automation-dashboard/styles/patterns/img/wf-icons/import_data.png")
        proactive_task.addGenericInformation("task.documentation", "PAIO/PAIOUserGuide.html#_import_data")
        self._addDefaultTaskSettings(proactive_task, __task_enabled, __work_dir, __limit_output_view, __precious_result)
        return proactive_task

    def create_Import_Data_And_Automate_Feature_Engineering_task(self, 
                                                                 import_from="PA:URL", 
                                                                 file_path="https://s3.eu-west-2.amazonaws.com/activeeon-public/datasets/pima-indians-diabetes.csv",
                                                                 file_delimiter=";",
                                                                 __task_enabled=True,
                                                                 __work_dir=".",
                                                                 __limit_output_view=100,
                                                                 __precious_result=True):
        """
        Create the Import_Data_And_Automate_Feature_Engineering task
        Assist data scientists to successfully load and encode their categorical data
        :return: A Python ProactiveTask object
        """
        proactive_task = self._gateway.createPythonTask()
        proactive_task.setTaskName("Import_Data_And_Automate_Feature_Engineering")
        proactive_task.addVariable("IMPORT_FROM", import_from)
        proactive_task.addVariable("FILE_PATH", file_path)
        proactive_task.addVariable("FILE_DELIMITER", file_delimiter)
        proactive_task.setTaskImplementationFromURL(self._base_url + "/catalog/buckets/ai-machine-learning/resources/Import_Data_And_Automate_Feature_Engineering_Script/raw")
        proactive_task.addGenericInformation("task.icon", "/automation-dashboard/styles/patterns/img/wf-icons/data-processing.png")
        proactive_task.addGenericInformation("task.documentation", "PAIO/PAIOUserGuide.html#_import_data_and_automate_feature_engineering")
        self._addDefaultTaskSettings(proactive_task, __task_enabled, __work_dir, __limit_output_view, __precious_result)
        return proactive_task

    def create_Import_Model_task(self, 
                                 model_url="https://s3.eu-west-2.amazonaws.com/activeeon-public/models/pima-indians-diabetes.model",
                                 __task_enabled=True,
                                 __work_dir=".",
                                 __limit_output_view=-1,
                                 __precious_result=True):
        """
        Create the Import_Model task
        Load a trained model, and use the model to make predictions for new data
        :return: A Python ProactiveTask object
        """
        proactive_task = self._gateway.createPythonTask()
        proactive_task.setTaskName("Import_Model")
        proactive_task.addVariable("MODEL_URL", model_url)
        proactive_task.setTaskImplementationFromURL(self._base_url + "/catalog/buckets/ai-machine-learning/resources/Import_Model_Script/raw")
        proactive_task.addGenericInformation("task.icon", "/automation-dashboard/styles/patterns/img/wf-icons/load_model.png")
        proactive_task.addGenericInformation("task.documentation", "PAIO/PAIOUserGuide.html#_import_model")
        self._addDefaultTaskSettings(proactive_task, __task_enabled, __work_dir, __limit_output_view, __precious_result)
        return proactive_task

    def create_Log_Parser_task(self, 
                               log_file_url="https://s3.eu-west-2.amazonaws.com/activeeon-public/datasets/HDFS_2k.log",
                               patterns_file_url="https://s3.eu-west-2.amazonaws.com/activeeon-public/datasets/patterns.csv",
                               structured_log_file_extension="HTML",
                               __task_enabled=True,
                               __work_dir=".",
                               __limit_output_view=-1,
                               __precious_result=True):
        """
        Create the Log_Parser task
        Extract a group of event templates, whereby raw logs can be structured
        :return: A Python ProactiveTask object
        """
        proactive_task = self._gateway.createPythonTask()
        proactive_task.setTaskName("Log_Parser")
        proactive_task.addVariable("LOG_FILE", log_file_url)
        proactive_task.addVariable("PATTERNS_FILE", patterns_file_url)
        proactive_task.addVariable("STRUCTURED_LOG_FILE", structured_log_file_extension)
        proactive_task.setTaskImplementationFromURL(self._base_url + "/catalog/buckets/ai-machine-learning/resources/Log_Parser_Script/raw")
        proactive_task.addGenericInformation("task.icon", "/automation-dashboard/styles/patterns/img/wf-icons/log_parser.png")
        proactive_task.addGenericInformation("task.documentation", "PAIO/PAIOUserGuide.html#_log_parser")
        self._addDefaultTaskSettings(proactive_task, __task_enabled, __work_dir, __limit_output_view, __precious_result)
        return proactive_task

    def create_Preview_Results_task(self,
                                    output_type="HTML",
                                    __task_enabled=True,
                                    __work_dir=".",
                                    __limit_output_view=-1,
                                    __precious_result=True):
        """
        Create the Preview_Results task
        Preview the HTML results of the predictions generated by a classification, clustering or regression algorithm
        :return: A Python ProactiveTask object
        """
        proactive_task = self._gateway.createPythonTask()
        proactive_task.setTaskName("Preview_Results")
        proactive_task.addVariable("OUTPUT_TYPE", output_type)
        proactive_task.setTaskImplementationFromURL(self._base_url + "/catalog/buckets/ai-machine-learning/resources/Preview_Results_Script/raw")
        proactive_task.addGenericInformation("task.icon", "/automation-dashboard/styles/patterns/img/wf-icons/preview_results.png")
        proactive_task.addGenericInformation("task.documentation", "PAIO/PAIOUserGuide.html#_preview_results")
        self._addDefaultTaskSettings(proactive_task, __task_enabled, __work_dir, __limit_output_view, __precious_result)
        return proactive_task

    def create_Append_Data_task(self,
                                __task_enabled=True,
                                __work_dir=".",
                                __limit_output_view=5,
                                __precious_result=True):
        """
        Create the Append_Data task
        Append rows of other to the end of this frame, returning a new object. Columns not in this frame are added as new columns.
        :return: A Python ProactiveTask object
        """
        proactive_task = self._gateway.createPythonTask()
        proactive_task.setTaskName("Append_Data")
        proactive_task.setTaskImplementationFromURL(self._base_url + "/catalog/buckets/ai-machine-learning/resources/Append_Data_Script/raw")
        proactive_task.addGenericInformation("task.icon", "/automation-dashboard/styles/patterns/img/wf-icons/data-processing.png")
        proactive_task.addGenericInformation("task.documentation", "PAIO/PAIOUserGuide.html#_append_data")
        self._addDefaultTaskSettings(proactive_task, __task_enabled, __work_dir, __limit_output_view, __precious_result)
        return proactive_task

    def create_Drop_Columns_task(self,
                                 columns_name="",
                                 __task_enabled=True,
                                 __work_dir=".",
                                 __limit_output_view=5,
                                 __precious_result=True):
        """
        Create the Drop_Columns task
        Remove the specified columns from your data
        :return: A Python ProactiveTask object
        """
        proactive_task = self._gateway.createPythonTask()
        proactive_task.setTaskName("Drop_Columns")
        proactive_task.addVariable("COLUMNS_NAME", columns_name)
        proactive_task.setTaskImplementationFromURL(self._base_url + "/catalog/buckets/ai-machine-learning/resources/Drop_Columns_Script/raw")
        proactive_task.addGenericInformation("task.icon", "/automation-dashboard/styles/patterns/img/wf-icons/data-processing.png")
        proactive_task.addGenericInformation("task.documentation", "PAIO/PAIOUserGuide.html#_drop_columns")
        self._addDefaultTaskSettings(proactive_task, __task_enabled, __work_dir, __limit_output_view, __precious_result)
        return proactive_task

    def create_Encode_Data_task(self,
                                columns_name="",
                                __task_enabled=True,
                                __work_dir=".",
                                __limit_output_view=5,
                                __precious_result=True):
        """
        Create the Encode_Data task
        Encode the specified columns from the data
        :return: A Python ProactiveTask object
        """
        proactive_task = self._gateway.createPythonTask()
        proactive_task.setTaskName("Encode_Data")
        proactive_task.addVariable("COLUMNS_NAME", columns_name)
        proactive_task.setTaskImplementationFromURL(self._base_url + "/catalog/buckets/ai-machine-learning/resources/Encode_Data_Script/raw")
        proactive_task.addGenericInformation("task.icon", "/automation-dashboard/styles/patterns/img/wf-icons/data-processing.png")
        proactive_task.addGenericInformation("task.documentation", "PAIO/PAIOUserGuide.html#_encode_data")
        self._addDefaultTaskSettings(proactive_task, __task_enabled, __work_dir, __limit_output_view, __precious_result)
        return proactive_task

    def create_Fill_NaNs_task(self,
                              fill_value="",
                              __task_enabled=True,
                              __work_dir=".",
                              __limit_output_view=5,
                              __precious_result=True):
        """
        Create the Fill_NaNs task
        Replace all NaN elements of the data with a specified value
        :return: A Python ProactiveTask object
        """
        proactive_task = self._gateway.createPythonTask()
        proactive_task.setTaskName("Fill_NaNs")
        proactive_task.addVariable("FILL_MAP", fill_value)
        proactive_task.setTaskImplementationFromURL(self._base_url + "/catalog/buckets/ai-machine-learning/resources/Fill_Nans_Script/raw")
        proactive_task.addGenericInformation("task.icon", "/automation-dashboard/styles/patterns/img/wf-icons/data-processing.png")
        proactive_task.addGenericInformation("task.documentation", "PAIO/PAIOUserGuide.html#_fill_nans")
        self._addDefaultTaskSettings(proactive_task, __task_enabled, __work_dir, __limit_output_view, __precious_result)
        return proactive_task

    def create_Filter_Columns_task(self,
                                   columns_name="",
                                   __task_enabled=True,
                                   __work_dir=".",
                                   __limit_output_view=5,
                                   __precious_result=True):
        """
        Create the Filter_Columns task
        Filter the columns of your data based on the specified column names
        :return: A Python ProactiveTask object
        """
        proactive_task = self._gateway.createPythonTask()
        proactive_task.setTaskName("Filter_Columns")
        proactive_task.addVariable("COLUMNS_NAME", columns_name)
        proactive_task.setTaskImplementationFromURL(self._base_url + "/catalog/buckets/ai-machine-learning/resources/Filter_Columns_Script/raw")
        proactive_task.addGenericInformation("task.icon", "/automation-dashboard/styles/patterns/img/wf-icons/data-processing.png")
        proactive_task.addGenericInformation("task.documentation", "PAIO/PAIOUserGuide.html#_filter_columns")
        self._addDefaultTaskSettings(proactive_task, __task_enabled, __work_dir, __limit_output_view, __precious_result)
        return proactive_task

    def create_Merge_Data_task(self,
                               ref_column="",
                               __task_enabled=True,
                               __work_dir=".",
                               __limit_output_view=5,
                               __precious_result=True):
        """
        Create the Merge_Data task
        Merge two dataframes by performing a database-style join operation by columns or indexes
        :return: A Python ProactiveTask object
        """
        proactive_task = self._gateway.createPythonTask()
        proactive_task.setTaskName("Merge_Data")
        proactive_task.addVariable("REF_COLUMN", ref_column)
        proactive_task.setTaskImplementationFromURL(self._base_url + "/catalog/buckets/ai-machine-learning/resources/Merge_Data_Script/raw")
        proactive_task.addGenericInformation("task.icon", "/automation-dashboard/styles/patterns/img/wf-icons/data-processing.png")
        proactive_task.addGenericInformation("task.documentation", "PAIO/PAIOUserGuide.html#_merge_data")
        self._addDefaultTaskSettings(proactive_task, __task_enabled, __work_dir, __limit_output_view, __precious_result)
        return proactive_task

    def create_Query_Data_task(self,
                               query="",
                               __task_enabled=True,
                               __work_dir=".",
                               __limit_output_view=5,
                               __precious_result=True):
        """
        Create the Query_Data task
        Query the columns of a frame with a boolean expression
        :return: A Python ProactiveTask object
        """
        proactive_task = self._gateway.createPythonTask()
        proactive_task.setTaskName("Query_Data")
        proactive_task.addVariable("QUERY", query)
        proactive_task.setTaskImplementationFromURL(self._base_url + "/catalog/buckets/ai-machine-learning/resources/Query_Data_Script/raw")
        proactive_task.addGenericInformation("task.icon", "/automation-dashboard/styles/patterns/img/wf-icons/data-processing.png")
        proactive_task.addGenericInformation("task.documentation", "PAIO/PAIOUserGuide.html#_query_data")
        self._addDefaultTaskSettings(proactive_task, __task_enabled, __work_dir, __limit_output_view, __precious_result)
        return proactive_task

    def create_Rename_Columns_task(self,
                                   columns_name="",
                                   __task_enabled=True,
                                   __work_dir=".",
                                   __limit_output_view=5,
                                   __precious_result=True):
        """
        Create the Rename_Columns task
        Rename the columns of a dataframe
        :return: A Python ProactiveTask object
        """
        proactive_task = self._gateway.createPythonTask()
        proactive_task.setTaskName("Rename_Columns")
        proactive_task.addVariable("COLUMNS_NAME", columns_name)
        proactive_task.setTaskImplementationFromURL(self._base_url + "/catalog/buckets/ai-machine-learning/resources/Rename_Columns_Script/raw")
        proactive_task.addGenericInformation("task.icon", "/automation-dashboard/styles/patterns/img/wf-icons/data-processing.png")
        proactive_task.addGenericInformation("task.documentation", "PAIO/PAIOUserGuide.html#_rename_columns")
        self._addDefaultTaskSettings(proactive_task, __task_enabled, __work_dir, __limit_output_view, __precious_result)
        return proactive_task

    def create_Scale_Data_task(self,
                               scaler_name="RobustScaler",
                               columns_name="",
                               __task_enabled=True,
                               __work_dir=".",
                               __limit_output_view=5,
                               __precious_result=True):
        """
        Create the Scale_Data task
        Scale the specified columns from the data using the chosen scaler
        :return: A Python ProactiveTask object
        """
        proactive_task = self._gateway.createPythonTask()
        proactive_task.setTaskName("Scale_Data")
        proactive_task.addVariable("SCALER_NAME", scaler_name)
        proactive_task.addVariable("COLUMNS_NAME", columns_name)
        proactive_task.setTaskImplementationFromURL(self._base_url + "/catalog/buckets/ai-machine-learning/resources/Scale_Data_Script/raw")
        proactive_task.addGenericInformation("task.icon", "/automation-dashboard/styles/patterns/img/wf-icons/data-processing.png")
        proactive_task.addGenericInformation("task.documentation", "PAIO/PAIOUserGuide.html#_scale_data")
        self._addDefaultTaskSettings(proactive_task, __task_enabled, __work_dir, __limit_output_view, __precious_result)
        return proactive_task

    def create_Split_Data_task(self,
                               train_size=0.7,
                               __task_enabled=True,
                               __work_dir=".",
                               __limit_output_view=100,
                               __precious_result=True):
        """
        Create the Split_Data task
        Separate data into training and testing sets
        :return: A Python ProactiveTask object
        """
        proactive_task = self._gateway.createPythonTask()
        proactive_task.setTaskName("Split_Data")
        proactive_task.addVariable("TRAIN_SIZE", str(train_size))
        proactive_task.setTaskImplementationFromURL(self._base_url + "/catalog/buckets/ai-machine-learning/resources/Split_Data_Script/raw")
        proactive_task.addGenericInformation("task.icon", "/automation-dashboard/styles/patterns/img/wf-icons/data-processing.png")
        proactive_task.addGenericInformation("task.documentation", "PAIO/PAIOUserGuide.html#_split_data")
        self._addDefaultTaskSettings(proactive_task, __task_enabled, __work_dir, __limit_output_view, __precious_result)
        return proactive_task

    def create_Feature_Vector_Extractor_task(self,
                                             session_column="id_block",
                                             pattern_column="pattern_id",
                                             patterns_count_features=False,
                                             state_variables="status,date",
                                             count_variables="ip_from,ip_to,pid,date,time",
                                             state_count_features_variables=True,
                                             __task_enabled=True,
                                             __work_dir=".",
                                             __limit_output_view=100,
                                             __precious_result=True):
        """
        Create the Feature_Vector_Extractor task
        Encode structured data into numerical feature vectors whereby machine learning models can be applied.
        :return: A Python ProactiveTask object
        """
        proactive_task = self._gateway.createPythonTask()
        proactive_task.setTaskName("Feature_Vector_Extractor")
        proactive_task.addVariable("SESSION_COLUMN", session_column)
        proactive_task.addVariable("PATTERN_COLUMN", pattern_column)
        proactive_task.addVariable("PATTERNS_COUNT_FEATURES", str(patterns_count_features))
        proactive_task.addVariable("STATE_VARIABLES", state_variables)
        proactive_task.addVariable("COUNT_VARIABLES", count_variables)
        proactive_task.addVariable("STATE_COUNT_FEATURES_VARIABLES", str(state_count_features_variables))
        proactive_task.setTaskImplementationFromURL(self._base_url + "/catalog/buckets/ai-machine-learning/resources/Feature_Vector_Extractor_Script/raw")
        proactive_task.addGenericInformation("task.icon", "/automation-dashboard/styles/patterns/img/wf-icons/filled_filter.png")
        proactive_task.addGenericInformation("task.documentation", "PAIO/PAIOUserGuide.html#_feature_vector_extractor")
        self._addDefaultTaskSettings(proactive_task, __task_enabled, __work_dir, __limit_output_view, __precious_result)
        return proactive_task

    def create_Summarize_Data_task(self,
                                   global_model_type="KMeans",
                                   ref_column="",
                                   __task_enabled=True,
                                   __work_dir=".",
                                   __limit_output_view=5,
                                   __precious_result=True):
        """
        Create the Summarize_Data task
        Create a set of statistical measures that describe each column in the input data.
        :return: A Python ProactiveTask object
        """
        proactive_task = self._gateway.createPythonTask()
        proactive_task.setTaskName("Summarize_Data")
        proactive_task.addVariable("GLOBAL_MODEL_TYPE", global_model_type)
        proactive_task.addVariable("REF_COLUMN", ref_column)
        proactive_task.setTaskImplementationFromURL(self._base_url + "/catalog/buckets/ai-machine-learning/resources/Summarize_Data_Script/raw")
        proactive_task.addGenericInformation("task.icon", "/automation-dashboard/styles/patterns/img/wf-icons/filled_filter.png")
        proactive_task.addGenericInformation("task.documentation", "PAIO/PAIOUserGuide.html#_summarize_data")
        self._addDefaultTaskSettings(proactive_task, __task_enabled, __work_dir, __limit_output_view, __precious_result)
        return proactive_task

    def create_Time_Series_Feature_Extraction_task(self,
                                                   time_column="time",
                                                   ref_column="",
                                                   all_features=False,
                                                   __task_enabled=True,
                                                   __work_dir=".",
                                                   __limit_output_view=5,
                                                   __precious_result=True):
        """
        Create the Time_Series_Feature_Extraction task
        Extract features from time series data based on the TSFRESH python package.
        :return: A Python ProactiveTask object
        """
        proactive_task = self._gateway.createPythonTask()
        proactive_task.setTaskName("Time_Series_Feature_Extraction")
        proactive_task.addVariable("TIME_COLUMN", time_column)
        proactive_task.addVariable("REF_COLUMN", ref_column)
        proactive_task.addVariable("ALL_FEATURES", str(all_features))
        proactive_task.setTaskImplementationFromURL(self._base_url + "/catalog/buckets/ai-machine-learning/resources/Time_Series_Feature_Extraction_Script/raw")
        proactive_task.addGenericInformation("task.icon", "/automation-dashboard/styles/patterns/img/wf-icons/filled_filter.png")
        proactive_task.addGenericInformation("task.documentation", "PAIO/PAIOUserGuide.html#_tsfresh_features_extraction")
        self._addDefaultTaskSettings(proactive_task, __task_enabled, __work_dir, __limit_output_view, __precious_result)
        return proactive_task

    def create_Autosklearn_Classifier_task(self,
                                           task_time=30,
                                           run_time=27,
                                           sampling=True,
                                           sampling_strategy="cv",
                                           folds=5,
                                           __task_enabled=True,
                                           __work_dir=".",
                                           __limit_output_view=5,
                                           __precious_result=True):
        """
        Create the AutoSklearn_Classifier task.
        AutoSklearn Classifier leverages recent advances in Bayesian optimization, meta-learning and ensemble construction.
        :return: A Python ProactiveTask object
        """
        proactive_task = self._gateway.createPythonTask()
        proactive_task.setTaskName("AutoSklearn_Classifier")
        proactive_task.addVariable("TASK_TIME", str(task_time))
        proactive_task.addVariable("RUN_TIME", str(run_time))
        proactive_task.addVariable("SAMPLING", str(sampling))
        proactive_task.addVariable("SAMPLING_STRATEGY", sampling_strategy)
        proactive_task.addVariable("FOLDS", str(folds))
        proactive_task.setTaskImplementationFromURL(self._base_url + "/catalog/buckets/ai-machine-learning/resources/Autosklearn_Classifier_Script/raw")
        proactive_task.addGenericInformation("task.icon", "/automation-dashboard/styles/patterns/img/wf-icons/AutoML.png")
        proactive_task.addGenericInformation("task.documentation", "PAIO/PAIOUserGuide.html#_autosklearn_classifier")
        self._addDefaultTaskSettings(proactive_task, __task_enabled, __work_dir, __limit_output_view, __precious_result)
        return proactive_task

    def create_Autosklearn_Regressor_task(self,
                                          task_time=120,
                                          run_time=30,
                                          sampling=False,
                                          sampling_strategy="cv",
                                          folds=5,
                                          __task_enabled=True,
                                          __work_dir=".",
                                          __limit_output_view=5,
                                          __precious_result=True):
        """
        Create the AutoSklearn_Regressor task.
        AutoSklearn Regressor leverages recent advances in Bayesian optimization, meta-learning and ensemble construction.
        :return: A Python ProactiveTask object
        """
        proactive_task = self._gateway.createPythonTask()
        proactive_task.setTaskName("AutoSklearn_Regressor")
        proactive_task.addVariable("TASK_TIME", str(task_time))
        proactive_task.addVariable("RUN_TIME", str(run_time))
        proactive_task.addVariable("SAMPLING", str(sampling))
        proactive_task.addVariable("SAMPLING_STRATEGY", sampling_strategy)
        proactive_task.addVariable("FOLDS", str(folds))
        proactive_task.setTaskImplementationFromURL(self._base_url + "/catalog/buckets/ai-machine-learning/resources/Autosklearn_Regressor_Script/raw")
        proactive_task.addGenericInformation("task.icon", "/automation-dashboard/styles/patterns/img/wf-icons/AutoML.png")
        proactive_task.addGenericInformation("task.documentation", "PAIO/PAIOUserGuide.html#_autosklearn_regressor")
        self._addDefaultTaskSettings(proactive_task, __task_enabled, __work_dir, __limit_output_view, __precious_result)
        return proactive_task

    def create_TPOT_Classifier_task(self,
                                    generations=3,
                                    scoring="accuracy",
                                    cv=5,
                                    verbosity=1,
                                    __task_enabled=True,
                                    __work_dir=".",
                                    __limit_output_view=5,
                                    __precious_result=True):
        """
        Create the TPOT_Classifier task.
        TPOT Classifier uses intelligent search for pipelines containing supervised classification models, preprocessors,
        feature selection, and other estimators or transformers following the scikit-learn API.
        :return: A Python ProactiveTask object
        """
        proactive_task = self._gateway.createPythonTask()
        proactive_task.setTaskName("TPOT_Classifier")
        proactive_task.addVariable("GENERATIONS", str(generations))
        proactive_task.addVariable("SCORING", scoring)
        proactive_task.addVariable("CV", str(cv))
        proactive_task.addVariable("VERBOSITY", str(verbosity))
        proactive_task.setTaskImplementationFromURL(self._base_url + "/catalog/buckets/ai-machine-learning/resources/Tpot_Classifier_Script/raw")
        proactive_task.addGenericInformation("task.icon", "/automation-dashboard/styles/patterns/img/wf-icons/AutoML.png")
        proactive_task.addGenericInformation("task.documentation", "PAIO/PAIOUserGuide.html#_tpot_classifier")
        self._addDefaultTaskSettings(proactive_task, __task_enabled, __work_dir, __limit_output_view, __precious_result)
        return proactive_task

    def create_TPOT_Regressor_task(self,
                                   generations=2,
                                   cv=5,
                                   scoring="neg_mean_squared_error",
                                   verbosity=1,
                                   __task_enabled=True,
                                   __work_dir=".",
                                   __limit_output_view=5,
                                   __precious_result=True):
        """
        Create the TPOT_Regressor task.
        TPOT Regressor uses intelligent search for pipelines containing supervised regression models, preprocessors,
        feature selection, and other estimators or transformers following the scikit-learn API.
        :return: A Python ProactiveTask object
        """
        proactive_task = self._gateway.createPythonTask()
        proactive_task.setTaskName("TPOT_Regressor")
        proactive_task.addVariable("GENERATIONS", str(generations))
        proactive_task.addVariable("CV", str(cv))
        proactive_task.addVariable("SCORING", scoring)
        proactive_task.addVariable("VERBOSITY", str(verbosity))
        proactive_task.setTaskImplementationFromURL(self._base_url + "/catalog/buckets/ai-machine-learning/resources/Tpot_Regressor_Script/raw")
        proactive_task.addGenericInformation("task.icon", "/automation-dashboard/styles/patterns/img/wf-icons/AutoML.png")
        proactive_task.addGenericInformation("task.documentation", "PAIO/PAIOUserGuide.html#_tpot_regressor")
        self._addDefaultTaskSettings(proactive_task, __task_enabled, __work_dir, __limit_output_view, __precious_result)
        return proactive_task

    def create_Gaussian_Naive_Bayes_task(self,
                                         input_variables="{}",
                                         scoring="accuracy",
                                         __task_enabled=True,
                                         __work_dir=".",
                                         __limit_output_view=5,
                                         __precious_result=True):
        """
        Create the Gaussian_Naive_Bayes task.
        Naive Bayes is a simple probabilistic classifier based on applying Bayes' theorem with strong independence assumptions.
        :return: A Python ProactiveTask object
        """
        proactive_task = self._gateway.createPythonTask()
        proactive_task.setTaskName("Gaussian_Naive_Bayes")
        proactive_task.addVariable("INPUT_VARIABLES", input_variables)
        proactive_task.addVariable("SCORING", scoring)
        proactive_task.setTaskImplementationFromURL(self._base_url + "/catalog/buckets/ai-machine-learning/resources/Gaussian_Naive_Bayes_Script/raw")
        proactive_task.addGenericInformation("task.icon", "/automation-dashboard/styles/patterns/img/wf-icons/ml_classification.png")
        proactive_task.addGenericInformation("task.documentation", "PAIO/PAIOUserGuide.html#_gaussian_naive_bayes")
        self._addDefaultTaskSettings(proactive_task, __task_enabled, __work_dir, __limit_output_view, __precious_result)
        return proactive_task

    def create_Logistic_Regression_task(self,
                                        input_variables="{}",
                                        scoring="accuracy",
                                        __task_enabled=True,
                                        __work_dir=".",
                                        __limit_output_view=5,
                                        __precious_result=True):
        """
        Create the Logistic_Regression task.
        Logistic Regression is a regression model where the Dependent Variable (DV) is categorical.
        :return: A Python ProactiveTask object
        """
        proactive_task = self._gateway.createPythonTask()
        proactive_task.setTaskName("Logistic_Regression")
        proactive_task.addVariable("INPUT_VARIABLES", input_variables)
        proactive_task.addVariable("SCORING", scoring)
        proactive_task.setTaskImplementationFromURL(self._base_url + "/catalog/buckets/ai-machine-learning/resources/Logistic_Regression_Script/raw")
        proactive_task.addGenericInformation("task.icon", "/automation-dashboard/styles/patterns/img/wf-icons/ml_classification.png")
        proactive_task.addGenericInformation("task.documentation", "PAIO/PAIOUserGuide.html#_logistic_regression")
        self._addDefaultTaskSettings(proactive_task, __task_enabled, __work_dir, __limit_output_view, __precious_result)
        return proactive_task

    def create_Support_Vector_Machines_task(self,
                                            input_variables="{\"probability\": true}",
                                            __task_enabled=True,
                                            __work_dir=".",
                                            __limit_output_view=5,
                                            __precious_result=True):
        """
        Create the Support_Vector_Machines task.
        Support Vector Machines are supervised learning models with associated learning algorithms used for classification.
        :return: A Python ProactiveTask object
        """
        proactive_task = self._gateway.createPythonTask()
        proactive_task.setTaskName("Support_Vector_Machines")
        proactive_task.addVariable("INPUT_VARIABLES", input_variables)
        proactive_task.setTaskImplementationFromURL(self._base_url + "/catalog/buckets/ai-machine-learning/resources/Support_Vector_Machine_Script/raw")
        proactive_task.addGenericInformation("task.icon", "/automation-dashboard/styles/patterns/img/wf-icons/ml_classification.png")
        proactive_task.addGenericInformation("task.documentation", "PAIO/PAIOUserGuide.html#_support_vector_machines")
        self._addDefaultTaskSettings(proactive_task, __task_enabled, __work_dir, __limit_output_view, __precious_result)
        return proactive_task

    def create_Bayesian_Ridge_Regression_task(self,
                                              input_variables="{}",
                                              __task_enabled=True,
                                              __work_dir=".",
                                              __limit_output_view=5,
                                              __precious_result=True):
        """
        Create the Bayesian_Ridge_Regression task.
        Bayesian Linear Regression is an approach to linear regression in which the statistical analysis is undertaken within the context of Bayesian inference.
        :return: A Python ProactiveTask object
        """
        proactive_task = self._gateway.createPythonTask()
        proactive_task.setTaskName("Bayesian_Ridge_Regression")
        proactive_task.addVariable("INPUT_VARIABLES", input_variables)
        proactive_task.setTaskImplementationFromURL(self._base_url + "/catalog/buckets/ai-machine-learning/resources/Bayesian_Ridge_Regression_Script/raw")
        proactive_task.addGenericInformation("task.icon", "/automation-dashboard/styles/patterns/img/wf-icons/ml_regresssion.png")
        proactive_task.addGenericInformation("task.documentation", "PAIO/PAIOUserGuide.html#_bayesian_ridge_regression")
        self._addDefaultTaskSettings(proactive_task, __task_enabled, __work_dir, __limit_output_view, __precious_result)
        return proactive_task

    def create_Linear_Regression_task(self,
                                      input_variables="{}",
                                      __task_enabled=True,
                                      __work_dir=".",
                                      __limit_output_view=5,
                                      __precious_result=True):
        """
        Create the Linear_Regression task.
        Linear Regression is useful for finding the relationship between a scalar dependent variable y and one or more explanatory variables (or independent variables) denoted X.
        :return: A Python ProactiveTask object
        """
        proactive_task = self._gateway.createPythonTask()
        proactive_task.setTaskName("Linear_Regression")
        proactive_task.addVariable("INPUT_VARIABLES", input_variables)
        proactive_task.setTaskImplementationFromURL(self._base_url + "/catalog/buckets/ai-machine-learning/resources/Linear_Regression_Script/raw")
        proactive_task.addGenericInformation("task.icon", "/automation-dashboard/styles/patterns/img/wf-icons/ml_regresssion.png")
        proactive_task.addGenericInformation("task.documentation", "PAIO/PAIOUserGuide.html#_linear_regression")
        self._addDefaultTaskSettings(proactive_task, __task_enabled, __work_dir, __limit_output_view, __precious_result)
        return proactive_task

    def create_Support_Vector_Regression_task(self,
                                              input_variables="{}",
                                              __task_enabled=True,
                                              __work_dir=".",
                                              __limit_output_view=5,
                                              __precious_result=True):
        """
        Create the Support_Vector_Regression task.
        Support Vector Regression are supervised learning models with associated learning algorithms that analyze data used for regression.
        :return: A Python ProactiveTask object
        """
        proactive_task = self._gateway.createPythonTask()
        proactive_task.setTaskName("Support_Vector_Regression")
        proactive_task.addVariable("INPUT_VARIABLES", input_variables)
        proactive_task.setTaskImplementationFromURL(self._base_url + "/catalog/buckets/ai-machine-learning/resources/Support_Vector_Regression_Script/raw")
        proactive_task.addGenericInformation("task.icon", "/automation-dashboard/styles/patterns/img/wf-icons/ml_regresssion.png")
        proactive_task.addGenericInformation("task.documentation", "PAIO/PAIOUserGuide.html#_support_vector_regression")
        self._addDefaultTaskSettings(proactive_task, __task_enabled, __work_dir, __limit_output_view, __precious_result)
        return proactive_task

    def create_K_Means_task(self,
                            input_variables="{\"n_clusters\": 2}",
                            __task_enabled=True,
                            __work_dir=".",
                            __limit_output_view=5,
                            __precious_result=True):
        """
        Create the K_Means task.
        K-means aims to partition n observations into k clusters in which each observation belongs to the cluster with the nearest mean, serving as a prototype of the cluster.
        :return: A Python ProactiveTask object
        """
        proactive_task = self._gateway.createPythonTask()
        proactive_task.setTaskName("K_Means")
        proactive_task.addVariable("INPUT_VARIABLES", input_variables)
        proactive_task.setTaskImplementationFromURL(self._base_url + "/catalog/buckets/ai-machine-learning/resources/K_means_Script/raw")
        proactive_task.addGenericInformation("task.icon", "/automation-dashboard/styles/patterns/img/wf-icons/ml_clustering.png")
        proactive_task.addGenericInformation("task.documentation", "PAIO/PAIOUserGuide.html#_kmeans")
        self._addDefaultTaskSettings(proactive_task, __task_enabled, __work_dir, __limit_output_view, __precious_result)
        return proactive_task

    def create_Mean_Shift_task(self,
                               input_variables="{}",
                               __task_enabled=True,
                               __work_dir=".",
                               __limit_output_view=5,
                               __precious_result=True):
        """
        Create the Mean_Shift task.
        Mean Shift is a non-parametric feature-space analysis technique for locating the maxima of a density function.
        :return: A Python ProactiveTask object
        """
        proactive_task = self._gateway.createPythonTask()
        proactive_task.setTaskName("Mean_Shift")
        proactive_task.addVariable("INPUT_VARIABLES", input_variables)
        proactive_task.setTaskImplementationFromURL(self._base_url + "/catalog/buckets/ai-machine-learning/resources/Mean_Shift_Script/raw")
        proactive_task.addGenericInformation("task.icon", "/automation-dashboard/styles/patterns/img/wf-icons/ml_clustering.png")
        proactive_task.addGenericInformation("task.documentation", "PAIO/PAIOUserGuide.html#_mean_shift")
        self._addDefaultTaskSettings(proactive_task, __task_enabled, __work_dir, __limit_output_view, __precious_result)
        return proactive_task

    def create_Isolation_Forest_task(self,
                                     input_variables="{}",
                                     __task_enabled=True,
                                     __work_dir=".",
                                     __limit_output_view=5,
                                     __precious_result=True):
        """
        Create the Isolation_Forest task.
        Isolation Forest isolates observations by randomly selecting a feature and then randomly selecting a split value between the maximum and minimum values of the selected feature.
        :return: A Python ProactiveTask object
        """
        proactive_task = self._gateway.createPythonTask()
        proactive_task.setTaskName("Isolation_Forest")
        proactive_task.addVariable("INPUT_VARIABLES", input_variables)
        proactive_task.setTaskImplementationFromURL(self._base_url + "/catalog/buckets/ai-machine-learning/resources/Isolation_Forest_Script/raw")
        proactive_task.addGenericInformation("task.icon", "/automation-dashboard/styles/patterns/img/wf-icons/ml_anomaly.png")
        proactive_task.addGenericInformation("task.documentation", "PAIO/PAIOUserGuide.html#_isolation_forest")
        self._addDefaultTaskSettings(proactive_task, __task_enabled, __work_dir, __limit_output_view, __precious_result)
        return proactive_task

    def create_One_Class_SVM_task(self,
                                  input_variables="{}",
                                  __task_enabled=True,
                                  __work_dir=".",
                                  __limit_output_view=5,
                                  __precious_result=True):
        """
        Create the One_Class_SVM task.
        One-class SVM is an unsupervised algorithm that learns a decision function for novelty detection: classifying new data as similar or different to the training set.
        :return: A Python ProactiveTask object
        """
        proactive_task = self._gateway.createPythonTask()
        proactive_task.setTaskName("One_Class_SVM")
        proactive_task.addVariable("INPUT_VARIABLES", input_variables)
        proactive_task.setTaskImplementationFromURL(self._base_url + "/catalog/buckets/ai-machine-learning/resources/One_Class_Svm_Script/raw")
        proactive_task.addGenericInformation("task.icon", "/automation-dashboard/styles/patterns/img/wf-icons/ml_anomaly.png")
        proactive_task.addGenericInformation("task.documentation", "PAIO/PAIOUserGuide.html#_one_class_svm")
        self._addDefaultTaskSettings(proactive_task, __task_enabled, __work_dir, __limit_output_view, __precious_result)
        return proactive_task

    def create_Adaboost_task(self,
                             input_variables="{}",
                             algorithm_type="Classification",
                             __task_enabled=True,
                             __work_dir=".",
                             __limit_output_view=5,
                             __precious_result=True):
        """
        Create the AdaBoost task.
        AdaBoost combines a weak classifier algorithm into a single strong classifier.
        :return: A Python ProactiveTask object
        """
        proactive_task = self._gateway.createPythonTask()
        proactive_task.setTaskName("AdaBoost")
        proactive_task.addVariable("INPUT_VARIABLES", input_variables)
        proactive_task.addVariable("TYPE", algorithm_type)
        proactive_task.setTaskImplementationFromURL(self._base_url + "/catalog/buckets/ai-machine-learning/resources/AdaBoost_Script/raw")
        proactive_task.addGenericInformation("task.icon", "/automation-dashboard/styles/patterns/img/wf-icons/ml_ensemble.png")
        proactive_task.addGenericInformation("task.documentation", "PAIO/PAIOUserGuide.html#_adaboost")
        self._addDefaultTaskSettings(proactive_task, __task_enabled, __work_dir, __limit_output_view, __precious_result)
        return proactive_task

    def create_Catboost_task(self,
                             input_variables="{}",
                             algorithm_type="Classification",
                             __task_enabled=True,
                             __work_dir=".",
                             __limit_output_view=5,
                             __precious_result=True):
        """
        Create the CatBoost task.
        CatBoost is a gradient boosting algorithm that helps reduce overfitting and can be used for classification and regression.
        :return: A Python ProactiveTask object
        """
        proactive_task = self._gateway.createPythonTask()
        proactive_task.setTaskName("CatBoost")
        proactive_task.addVariable("INPUT_VARIABLES", input_variables)
        proactive_task.addVariable("TYPE", algorithm_type)
        proactive_task.setTaskImplementationFromURL(self._base_url + "/catalog/buckets/ai-machine-learning/resources/CatBoost_Script/raw")
        proactive_task.addGenericInformation("task.icon", "/automation-dashboard/styles/patterns/img/wf-icons/ml_ensemble.png")
        proactive_task.addGenericInformation("task.documentation", "PAIO/PAIOUserGuide.html#_catboost")
        self._addDefaultTaskSettings(proactive_task, __task_enabled, __work_dir, __limit_output_view, __precious_result)
        return proactive_task

    def create_Gradient_Boosting_task(self,
                                      input_variables="{}",
                                      algorithm_type="Classification",
                                      __task_enabled=True,
                                      __work_dir=".",
                                      __limit_output_view=5,
                                      __precious_result=True):
        """
        Create the Gradient Boosting task.
        Gradient Boosting is an algorithm for regression or classification problems. It produces a prediction model in the form of an ensemble of weak prediction models.
        :return: A Python ProactiveTask object
        """
        proactive_task = self._gateway.createPythonTask()
        proactive_task.setTaskName("Gradient_Boosting")
        proactive_task.addVariable("INPUT_VARIABLES", input_variables)
        proactive_task.addVariable("TYPE", algorithm_type)
        proactive_task.setTaskImplementationFromURL(self._base_url + "/catalog/buckets/ai-machine-learning/resources/Gradient_Boosting_Script/raw")
        proactive_task.addGenericInformation("task.icon", "/automation-dashboard/styles/patterns/img/wf-icons/ml_ensemble.png")
        proactive_task.addGenericInformation("task.documentation", "PAIO/PAIOUserGuide.html#_gradient_boosting")
        self._addDefaultTaskSettings(proactive_task, __task_enabled, __work_dir, __limit_output_view, __precious_result)
        return proactive_task

    def create_Random_Forest_task(self,
                                  input_variables="{}",
                                  algorithm_type="Classification",
                                  __task_enabled=True,
                                  __work_dir=".",
                                  __limit_output_view=5,
                                  __precious_result=True):
        """
        Create the Random Forest task.
        Random Forest is an algorithm for regression, classification, and other tasks that operates by constructing a multitude of decision trees at training time.
        :return: A Python ProactiveTask object
        """
        proactive_task = self._gateway.createPythonTask()
        proactive_task.setTaskName("Random_Forest")
        proactive_task.addVariable("INPUT_VARIABLES", input_variables)
        proactive_task.addVariable("TYPE", algorithm_type)
        proactive_task.setTaskImplementationFromURL(self._base_url + "/catalog/buckets/ai-machine-learning/resources/Random_Forest_Script/raw")
        proactive_task.addGenericInformation("task.icon", "/automation-dashboard/styles/patterns/img/wf-icons/ml_ensemble.png")
        proactive_task.addGenericInformation("task.documentation", "PAIO/PAIOUserGuide.html#_random_forest")
        self._addDefaultTaskSettings(proactive_task, __task_enabled, __work_dir, __limit_output_view, __precious_result)
        return proactive_task

    def create_XGBoost_task(self,
                            input_variables="{}",
                            algorithm_type="Classification",
                            __task_enabled=True,
                            __work_dir=".",
                            __limit_output_view=5,
                            __precious_result=True):
        """
        Create the XGBoost task.
        XGBoost is an implementation of gradient boosted decision trees designed for speed and performance.
        :return: A Python ProactiveTask object
        """
        proactive_task = self._gateway.createPythonTask()
        proactive_task.setTaskName("XGBoost")
        proactive_task.addVariable("INPUT_VARIABLES", input_variables)
        proactive_task.addVariable("TYPE", algorithm_type)
        proactive_task.setTaskImplementationFromURL(self._base_url + "/catalog/buckets/ai-machine-learning/resources/XGBoost_Script/raw")
        proactive_task.addGenericInformation("task.icon", "/automation-dashboard/styles/patterns/img/wf-icons/ml_ensemble.png")
        proactive_task.addGenericInformation("task.documentation", "PAIO/PAIOUserGuide.html#_xgboost")
        self._addDefaultTaskSettings(proactive_task, __task_enabled, __work_dir, __limit_output_view, __precious_result)
        return proactive_task

    def create_Train_Model_task(self,
                                label_column="",
                                n_splits=5,
                                __task_enabled=True,
                                __work_dir=".",
                                __limit_output_view=5,
                                __precious_result=True):
        """
        Create the Train_Model task.
        Train a classification/clustering/anomaly detection model.
        :return: A Python ProactiveTask object
        """
        proactive_task = self._gateway.createPythonTask()
        proactive_task.setTaskName("Train_Model")
        proactive_task.addVariable("LABEL_COLUMN", label_column)
        proactive_task.addVariable("N_SPLITS", str(n_splits))
        proactive_task.setTaskImplementationFromURL(self._base_url + "/catalog/buckets/ai-machine-learning/resources/Train_Model_Script/raw")
        proactive_task.addGenericInformation("task.icon", "/automation-dashboard/styles/patterns/img/wf-icons/train.png")
        proactive_task.addGenericInformation("task.documentation", "PAIO/PAIOUserGuide.html#_train_model")
        self._addDefaultTaskSettings(proactive_task, __task_enabled, __work_dir, __limit_output_view, __precious_result)
        pre_script = self._gateway.createPreScript(self._gateway.getProactiveScriptLanguage().groovy())
        pre_script.setImplementationFromURL(self._base_url + "/catalog/buckets/ai-auto-ml-optimization/resources/get_automl_token/raw")
        proactive_task.setPreScript(pre_script)
        return proactive_task

    def create_Predict_Model_task(self,
                                  label_column="",
                                  __task_enabled=True,
                                  __work_dir=".",
                                  __limit_output_view=100,
                                  __precious_result=True):
        """
        Create the Predict_Model task.
        Generate predictions using a trained model.
        :return: A Python ProactiveTask object
        """
        proactive_task = self._gateway.createPythonTask()
        proactive_task.setTaskName("Predict_Model")
        proactive_task.addVariable("LABEL_COLUMN", label_column)
        proactive_task.setTaskImplementationFromURL(self._base_url + "/catalog/buckets/ai-machine-learning/resources/Predict_Model_Script/raw")
        proactive_task.addGenericInformation("task.icon", "/automation-dashboard/styles/patterns/img/wf-icons/predict.png")
        proactive_task.addGenericInformation("task.documentation", "PAIO/PAIOUserGuide.html#_predict_model")
        self._addDefaultTaskSettings(proactive_task, __task_enabled, __work_dir, __limit_output_view, __precious_result)
        return proactive_task

    def create_Model_Explainability_task(self,
                                         label_column="",
                                         feature_partial_plots="",
                                         feature_partial2d_plots="",
                                         shap_row_show="",
                                         __task_enabled=True,
                                         __work_dir=".",
                                         __limit_output_view=100,
                                         __precious_result=True):
        """
        Create the Model_Explainability task.
        Allow to understand the model's global behavior or specific predictions.
        :return: A Python ProactiveTask object
        """
        proactive_task = self._gateway.createPythonTask()
        proactive_task.setTaskName("Model_Explainability")
        proactive_task.addVariable("LABEL_COLUMN", label_column)
        proactive_task.addVariable("FEATURE_PARTIAL_PLOTS", feature_partial_plots)
        proactive_task.addVariable("FEATURE_PARTIAL2D_PLOTS", feature_partial2d_plots)
        proactive_task.addVariable("SHAP_ROW_SHOW", shap_row_show)
        proactive_task.setTaskImplementationFromURL(self._base_url + "/catalog/buckets/ai-machine-learning/resources/Model_Explainability_Script/raw")
        proactive_task.addGenericInformation("task.icon", "/automation-dashboard/styles/patterns/img/wf-icons/model-explainability.png")
        proactive_task.addGenericInformation("task.documentation", "PAIO/PAIOUserGuide.html#_ml_explainability")
        self._addDefaultTaskSettings(proactive_task, __task_enabled, __work_dir, __limit_output_view, __precious_result)
        return proactive_task
