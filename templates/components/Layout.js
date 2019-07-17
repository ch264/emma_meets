
import Head from 'next/head'
import Navbar from '../components/Navbar'
import Footer from '../components/Footer'


const Layout = (props) => (
    <div>
        <Head>
            <title>EmmaMeets</title>
            {/* CDN Materialize */}
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css"/>
            <link rel="stylesheet" href="/static/index.css" />
        </Head>
        <Navbar /> 
        <div className="container">
            {props.children}
        </div>
        <Footer />
    </div>
)

export default Layout;