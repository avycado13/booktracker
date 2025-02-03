import React, { createContext, useContext } from "react";
import apiClient from "./apiClient";

const ApiClientContext = createContext(apiClient);

interface ApiClientProviderProps {
    children: React.ReactNode;
}

export const ApiClientProvider: React.FC<ApiClientProviderProps> = ({ children }) => {
    return (
        <ApiClientContext.Provider value={apiClient}>
            {children}
        </ApiClientContext.Provider>
    );
};

export const useApiClient = () => {
    return useContext(ApiClientContext);
};
