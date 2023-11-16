import { Alert } from "@mui/material";
import axios from "axios";
import md5 from "crypto-js/md5";
import PropTypes from "prop-types";
import React, { createContext, useCallback, useEffect, useMemo, useState } from "react";

// Create the Context
export const TopicsContext = createContext();

/**
 * Return a MD5 from the contents of a text file.
 * @param {Promise<FileReader>} file
 * @returns String
 */
async function hashPartialFile(file) {
  const reader = new FileReader();
  reader.readAsText(file);

  return new Promise((resolve, reject) => {
    reader.onload = async (event) => {
      const text = event.target.result;
      const lines = text.split("\n");

      let contentToHash;
      if (lines.length < 5) {
        // If less than 5 lines, use the entire content
        contentToHash = text;
      } else {
        // Otherwise, use the first two and the last two lines
        contentToHash = [...lines.slice(0, 2), ...lines.slice(-2)].join("\n");
      }

      // Compute MD5 hash
      const hash = md5(contentToHash).toString();
      resolve(hash);
    };

    reader.onerror = (error) => {
      reject(error);
    };
  });
}

/*
const saveDataToFile = (fileName, data) => {
  const blob = new Blob([data], { type: "application/json" });

  // Create a link element
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = fileName;

  // Trigger a click event to download the file
  a.click();
};
*/

const ENDPOINT_PATH = "/topics/csv";
// Fetcher function 
const fetcher = (url, data) => axios.post(url, data, {
  headers: {
    'Content-Type': 'multipart/form-data'
  }
}).then((res) => res.data);

// Provider Component
export function TopicsProvider({ children, onSelectView }) {
  const [isLoading, setIsLoading] = useState(false);
  const [data, setData] = useState();
  const [error, setError] = useState();
  const [errorText, setErrorText] = useState("");
  // Handle File Upload and POST Request
  const uploadFile = useCallback(
    async (file, params) => {
      setIsLoading(true);
      setErrorText("");

      try {
        // Generate SHA-256 hash of the file
        const fileHash = await hashPartialFile(file);

        const formData = new FormData();
        formData.append("file", file);
        // Append additional parameters to formData
        formData.append("n_clusters", params.n_clusters);
        formData.append("openapi_key", params.openapi_key);
        formData.append("selected_column", params.selected_column);

        const apiURI = `${process.env.REACT_APP_API_ENDPOINT}${ENDPOINT_PATH}?md5=${fileHash}`;
        // Perform the POST request
        const response = await fetcher(apiURI, formData);
        setData(response);
        // auto-switch to Map view
        if (onSelectView) onSelectView("map");
        // TODO Save topics and docs to files in the public directory
        // saveDataToFile("bunka_topics.json", JSON.stringify(data.topics));
        // saveDataToFile("bunka_docs.json", JSON.stringify(data.docs));
      } catch (errorExc) {
        // Handle error
        const errorMessage = errorExc.response?.data?.message || errorExc.message || 'An unknown error occurred';
        console.error('Error:', errorMessage);
        setErrorText(errorMessage);
        setError(errorExc.response);
      } finally {
        setIsLoading(false);
      }
    },
    [onSelectView, setErrorText, setError, setIsLoading, setData],
  );

  useEffect(() => {
    if (error !== undefined && error.length) {
      const message = error.response ? error.response.data.message : error.message;
      setErrorText(`Error uploading file.\n${message}`);
      console.error("Error uploading file:", message);
    }
  }, [error]);

  const providerValue = useMemo(
    () => ({
      data,
      uploadFile,
      isLoading,
      error,
    }),
    [data, uploadFile, isLoading, error],
  );

  return (
    <TopicsContext.Provider value={providerValue}>
      <>
        {isLoading && <div className="loader" />}
        {errorText && (
          <Alert severity="error" className="errorMessage">
            {errorText}
          </Alert>
        )}
        {children}
      </>
    </TopicsContext.Provider>
  );
}

TopicsProvider.propTypes = {
  children: PropTypes.func.isRequired,
  onSelectView: PropTypes.func.isRequired,
};
