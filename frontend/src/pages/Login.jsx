import '../styles/Login.css';
import axios from 'axios';
import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';

function Login(){
    const [user, setUser] = useState('');
    const [password, setPassword] = useState('');
    const [partition, setPartition] = useState('');
    const navigate = useNavigate(); 

    const handleSubmit = (e) => {
        e.preventDefault();
        axios.post('http://localhost:5000/api/login', {
            user: user,
            password: password,
            id_partition: partition
        }).then((response) => {
            if(response.data.status === 'success'){
                alert('Login exitoso');
                navigate('/reports');
            } else {
                alert(response.data.error);
            }
        }).catch((error) => {
            alert(error);
        });
    }

    return(
        <div className="Login">
            <section>
                <h1 className="login-title">Login</h1>

                <form className='formulario'>
                    <input className="input-log" type="text" placeholder="Usuario" value={user} onChange={(e) => {setUser(e.target.value)}}/>
                    <input className='input-log' type="password" placeholder="Contraseña" value={password} onChange={(e) => {setPassword(e.target.value)}}/>
                    <input className='input-log' type="partition" placeholder="ID Particion" value={partition} onChange={(e) => {setPartition(e.target.value)}}/>
                    <div className='buttons'>
                        <button type="submit" onClick={handleSubmit}>Ingresar</button>
                        <Link className='Link-origin' to='/'>
                            <button className='cancel'>Cancelar</button>
                        </Link>
                    </div>
                </form>
            </section>
        </div>
    )
}

export default Login;