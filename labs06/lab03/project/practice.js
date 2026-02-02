const processUsers = (users) => {
    if (!users || users.length === 0) {
        return {
            avgAge: 0,
            byCity: {},
            activeEmails: []
        };
    }
    
    const totalAge = users.reduce((sum, user) => sum + user.age, 0);
    const avgAge = totalAge / users.length;
    
    const byCity = users.reduce((acc, user) => {
        const city = user.city;
        acc[city] = (acc[city] || 0) + 1;
        return acc;
    }, {});
    
    const activeEmails = users
        .filter(user => user.active)
        .map(user => user.email);
    
    return {
        avgAge,
        byCity,
        activeEmails
    };
};

const useForm = (initialValues) => {
    let values = { ...initialValues };
    let errors = {};
    
    const setValue = (name, value) => {
        values = { ...values, [name]: value };
    };
    
    const setError = (name, error) => {
        errors = { ...errors, [name]: error };
    };
    
    const validate = () => {
        errors = {};
        if (!values.email) {
            errors.email = 'Email is required';
        }
        if (!values.name) {
            errors.name = 'Name is required';
        }
        return Object.keys(errors).length === 0;
    };
    
    const handleSubmit = (onSubmit) => {
        return (e) => {
            e.preventDefault();
            if (validate()) {
                onSubmit(values);
            }
        };
    };
    
    return {
        values,
        errors,
        setValue,
        setError,
        handleSubmit,
        validate
    };
};

const debounce = (func, delay) => {
    let timeoutId;
    return (...args) => {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => func.apply(null, args), delay);
    };
};

const users = [
    { name: 'John', age: 25, city: 'New York', active: true, email: 'john@example.com' },
    { name: 'Jane', age: 30, city: 'Boston', active: false, email: 'jane@example.com' },
    { name: 'Bob', age: 28, city: 'New York', active: true, email: 'bob@example.com' }
];

console.log('=== Практические задания ===');
console.log('Обработка пользователей:', processUsers(users));

const form = useForm({ name: '', email: '' });
form.setValue('name', 'Test User');
form.setValue('email', 'test@example.com');
console.log('Форма:', form.values);
console.log('Валидация:', form.validate());

const debouncedLog = debounce((msg) => console.log('Debounced:', msg), 1000);
debouncedLog('Message 1');
debouncedLog('Message 2');
setTimeout(() => debouncedLog('Message 3'), 500);

