// Import React library
import React, { useState, useEffect } from 'react';

// Define a functional component
const Qa = () => {
    const [inputValue, setInputValue] = useState(localStorage.getItem('inputValue') || '');
    const [response, setResponse] = useState(JSON.parse(localStorage.getItem('response')) || null);
    const [isLoading, setIsLoading] = useState(false);

    useEffect(() => {
        localStorage.setItem('inputValue', inputValue);
    }, [inputValue]);

    useEffect(() => {
        localStorage.setItem('response', JSON.stringify(response));
    }, [response]);

    const handleSubmit = async (event) => {
        console.log("handleSubmit.........");
        event.preventDefault();
        setIsLoading(true); // Set loading state to true
        try {
            const response = await fetch(`/query?query=${inputValue}`, {
                method: 'POST',
                headers: {
                    'accept': 'application/json',
                },
                body: ''
            });
            const result = await response.json();
            console.log(result);
            setResponse(result);
        } catch (error) {
            console.error('Error:', error);
        } finally {
            setIsLoading(false); // Set loading state to false
        }
    };

    return (
        <div>
            <h1>Input your questions:</h1>
            <form onSubmit={handleSubmit}>
                <input 
                    type="text" 
                    value={inputValue} 
                    onChange={(e) => setInputValue(e.target.value)} 
                    style={{ width: '400px' }} // Increase the input box length
                    disabled={isLoading} // Disable the input when loading
                />
                <button type="submit" disabled={isLoading}>
                    {isLoading ? 'Please wait...' : 'Submit'}
                </button>
            </form>
            {isLoading && <p style={{ color: 'red' }}>Please wait...</p>}
            {response && (
                <div style={{ width: '80%' }}>
                    <h2>Response:</h2>
                    <p style={{ width: '100%' }}>
                        {JSON.stringify(response, null, 2)}
                    </p>
                </div>
            )}
        </div>
    );
};

// Export the component so that it can be used in other files
export default Qa;