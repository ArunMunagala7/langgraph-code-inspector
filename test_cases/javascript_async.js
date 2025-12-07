# Test Case: JavaScript Async/Await Pattern
# Expected Quality: B+
# Expected Bugs: 1


// Async data fetching with error handling
async function fetchUserData(userId) {
    try {
        const response = await fetch(`/api/users/${userId}`);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Failed to fetch user:', error);
        return null;
    }
}

// Bug: No error handling for Promise.all
async function fetchMultipleUsers(userIds) {
    const promises = userIds.map(id => fetchUserData(id));
    const results = await Promise.all(promises);  // Could fail if any promise rejects
    return results.filter(user => user !== null);
}

// Good: Proper error handling with Promise.allSettled
async function fetchMultipleUsersSafe(userIds) {
    const promises = userIds.map(id => fetchUserData(id));
    const results = await Promise.allSettled(promises);
    
    return results
        .filter(result => result.status === 'fulfilled')
        .map(result => result.value)
        .filter(user => user !== null);
}
