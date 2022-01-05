import { useState, createContext, useContext } from "react";

export const CustomerContext = createContext([]);

export const useCustomer = () => useContext(CustomerContext);

export const CustomerWrapper = ({ children }) => {
  const [customer, setCustomer] = useState(null);
  const [working, setWorking] = useState(true);


  return (
    <CustomerContext.Provider value={{ customer, setCustomer }}>
      {working ? null : children}
    </CustomerContext.Provider>
  );
};