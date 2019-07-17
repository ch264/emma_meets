import Layout from '../components/Layout';

const About = () => (
    <Layout>
        <div>
            <h1>About EmmaMeets</h1>
            <img src="#" alt="Emma on Grass"></img>
            <p>Emma Meets was created to provide a social media platform, for dog owners to find and leave reviews for dog related products.Emma is a 14 year old spaniel who loves to meet other dogs and share her experience with dog products that she uses. These include dog Hotels, pet insurances, dog fashion and many more. Join us for free and find what works best for other dogs! Or share your review to contribute to our community. Feel free to browse reviews created by the community and save them to your favorites! Just sign up for an account to get started or login if you already have an account. Happy woof!</p>
        </div>

        <div class="row">
            <div class="col s6">
                <div class="card">
                    <div class="card-image">
                    <img src="images/sample-1.jpg" alt="emma"/>
                    <span class="card-title">Meet Emma</span>
                    </div>
                    <div class="card-content">
                    <p>Emma was born in 2004 into a puppy trading organisation. She was kept in isolation in a cellar and used as a puppy breeding machine for the first four years of her life. When finally someone reported the breeders, the police rescued the dogs and we took Emma in. When Emma came to us in 2007 she did not know the feeling of grass below her paws, what snow felt like or how to interact with other dogs. Since then she has come a very long way. Emma has learned how to play, how to swim in a lake, how to hike up mountains and sniff along the way and how good it is to cuddle for hours on the couch. We love her very much and want to share all the products that make her life easier. Emma looooves her yellow raincoat and will not go outside without it, because it has a hoodie that keeps her ears dry.</p>
                    </div>
                </div>
            </div>

            <div class="col s6">
                <div class="card">
                    <div class="card-image">
                    <img src="images/sample-1.jpg" alt="christina and emma"/>
                    <span class="card-title">Meet Christina</span>
                    </div>
                    <div class="card-content">
                    <p>Christina is a former Cell and Molecular Biologist, DNA expert and Customer Success Manager turned Full Stack Developer. With a continuous drive to learn and craving for knowledge, she has a passion for products that provide meaningful value. With her love for Emma and striving to make her live as pleasant as possible Christina is always on the lookout for dog related products. Lets create a community help each other to choose only the best for our puppies by leaving an honest review about dog related products.</p>
                    </div>
                    <div class="card-action">
                    <a href="#">Christina's GitHub</a>
                    </div>
                </div>
            </div>
        </div>
    </Layout>
)

export default About