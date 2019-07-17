import Link from 'next/link';

const Navbar = () => (
    <nav>
        <div class="nav-wrapper active">
            <a href='/' class="brand-logo"><img class="responsive-img" src="./static/customIcon.png" alt="dog"/></a>
            <ul id="nav-mobile" class="right hide-on-med-and-down">
                <li className="nav-item">
                <Link href="/"><a className="nav-link">Home</a></Link>
                </li>
                <li className="nav-item">
                <Link href="/about"><a className="nav-link">About</a></Link>
                </li>
                <li className="nav-item">
                <Link href="/contactus"><a className="nav-link">Contact Us</a></Link>
                </li>
                <li className="nav-item">
                <Link href="/products"><a className="nav-link">Products</a></Link>
                </li>
                <li className="nav-item">
                <Link href="/login"><a className="nav-link">login</a></Link>
                </li>
                <li className="nav-item">
                <Link href="/signup"><a className="nav-link">Signup</a></Link>
                </li>
            </ul>
        </div>
    </nav>
)

export default Navbar