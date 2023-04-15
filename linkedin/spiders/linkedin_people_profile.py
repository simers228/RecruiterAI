import scrapy

class LinkedInPeopleProfileSpider(scrapy.Spider):
    name = "linkedin_people_profile"

    custom_settings = {
        'FEEDS': { 'data/%(name)s_%(time)s.jsonl': { 'format': 'jsonlines',}}
        }

    def start_requests(self):
        profile_list = ['catherine-ainikkal-146a0510a','rachel-marshall-montavon-68604526', 'nmarion1', 'adriana-campa-134153149','ray-beckman-p-e-067652a2',
                        'joe-nikolai-084110114', 'agratha-reddy-8a6048113','eszter-csicsai-94a2096b', 'ali-noel-406447218','justin-johnson-pe-cxa-598b0a91',
                         'angelaberes', 'nicholas-knoke-gsp-792b93130', 'joshua-koss-gsp-7615291a2', 'ryan-clinton-145ab018a','mike-baccus-cet-30a772141', 
                         'paul-wick', 'andrew-roensch-43b866a2', 'keith-mcnamee-60031129', 'brian-filiatrault-1638a391', 'paul-petit-079282b6', 
                         'alfred-ladores-88873198', 'tayler-budenski-matzke-05404080','danielle-breva-81071732', 'danae-ticey-moore-9637a834', 'jordanxhuang', 
                         'allison-oyos-b76686102','meg-anderson-51b0698', 'paul-noll-8832518a', 'charles-lentz-bb908727', 'tim-kittila-p-e-5b36888', 
                         'david-santos-15a484114','dan-blossey-68383938', 'jimmy-garcia-3b947a192', 'alexander-vera-b8762284', 'weston-kolles-57a568130',
                         'taylor-boileau', 'michael-dahdal-771b53181', 'alberto-martinez28', 'kjmaki', 'jesse-peralta-0496971b1',
                         'paulkieffer', 'ian-dolph-6b8060128', 'todd-hensley-49887b77', 'dean-rossi-2824b985', 'kirk-blasdel-1b2b2581',
                         'patrick-sims-b7b59183', 'jeff-martin-a88a8a30', 'lucas-hubbard-742110167', 'randy-berner-b831367', 'michael-ortiz-b2806232',
                         'john-huyett-pe', 'caleb-frost', 'chrisannzeller', 'lindsey-van-vuuren', 'carol-spalony-34408a4a',
                         'aaric-witt-2a279412a', 'pcdodds', 'steven-jackson-ab029679', 'ben-r-bowman', 'carlakolber',
                         'melissa-montiel-a21181176', 'terry-stewart-csp-csm-b-a-s-etc-15306616b', 'keith-burch-983264122', 'bob-millerbernd-a9335a241', 'andy-brown-861ba097',
                         'jose-chavez-8146821a1', 'josh-helgesen-605b5195', 'jacob-machone-pe-19a04661', 'chrisbristowgreiner', 'aleisha-kiley-46ba7462',
                         'josh-miltenberger-033799a', 'spencer-greiner-86463554', 'bryce-williamson-6483262a', 'adam-allison-dpt-coss-75b40914a', 'yalda-akbarpour',
                         'mark-close', 'jessica-venegas-9bb01968', 'tim-benbow-92a34698', 'anthonykriens', 'asha-garcia-87b239b3'
                         ]
        for profile in profile_list:
            linkedin_people_url = f'https://www.linkedin.com/in/{profile}/' 
            yield scrapy.Request(url=linkedin_people_url, callback=self.parse_profile, meta={'profile': profile, 'linkedin_url': linkedin_people_url})

    def parse_profile(self, response):
        item = {}
        item['profile'] = response.meta['profile']
        item['url'] = response.meta['linkedin_url']

        """
            SUMMARY SECTION
        """
        summary_box = response.css("section.top-card-layout")
        item['name'] = summary_box.css("h1::text").get().strip()
        item['description'] = summary_box.css("h2::text").get().strip()

        ## Location
        try:
            item['location'] = summary_box.css('div.top-card__subline-item::text').get()
        except:
            item['location'] = summary_box.css('span.top-card__subline-item::text').get().strip()
            if 'followers' in item['location'] or 'connections' in item['location']:
                item['location'] = ''

        item['followers'] = ''
        item['connections'] = ''

        for span_text in summary_box.css('span.top-card__subline-item::text').getall():
            if 'followers' in span_text:
                item['followers'] = span_text.replace(' followers', '').strip()
            if 'connections' in span_text:
                item['connections'] = span_text.replace(' connections', '').strip()


        """
            ABOUT SECTION
        """
        item['about'] = response.css('section.summary div.core-section-container__content p::text').get()


        """
            EXPERIENCE SECTION
        """
        item['experience'] = []
        experience_blocks = response.css('li.experience-item')
        for block in experience_blocks:
            experience = {}
            ## organisation profile url
            try:
                experience['organisation_profile'] = block.css('h4 a::attr(href)').get().split('?')[0]
            except Exception as e:
                print('experience --> organisation_profile', e)
                experience['organisation_profile'] = ''
                
                
            ## location
            try:
                experience['location'] = block.css('p.experience-item__location::text').get().strip()
            except Exception as e:
                print('experience --> location', e)
                experience['location'] = ''
                
                
            ## description
            try:
                experience['description'] = block.css('p.show-more-less-text__text--more::text').get().strip()
            except Exception as e:
                print('experience --> description', e)
                try:
                    experience['description'] = block.css('p.show-more-less-text__text--less::text').get().strip()
                except Exception as e:
                    print('experience --> description', e)
                    experience['description'] = ''
                    
            ## time range
            try:
                date_ranges = block.css('span.date-range time::text').getall()
                if len(date_ranges) == 2:
                    experience['start_time'] = date_ranges[0]
                    experience['end_time'] = date_ranges[1]
                    experience['duration'] = block.css('span.date-range__duration::text').get()
                elif len(date_ranges) == 1:
                    experience['start_time'] = date_ranges[0]
                    experience['end_time'] = 'present'
                    experience['duration'] = block.css('span.date-range__duration::text').get()
            except Exception as e:
                print('experience --> time ranges', e)
                experience['start_time'] = ''
                experience['end_time'] = ''
                experience['duration'] = ''
            
            item['experience'].append(experience)

        
        """
            EDUCATION SECTION
        """
        item['education'] = []
        education_blocks = response.css('li.education__list-item')
        for block in education_blocks:
            education = {}

            ## organisation
            try:
                education['organisation'] = block.css('h3::text').get().strip()
            except Exception as e:
                print("education --> organisation", e)
                education['organisation'] = ''


            ## organisation profile url
            try:
                education['organisation_profile'] = block.css('a::attr(href)').get().split('?')[0]
            except Exception as e:
                print("education --> organisation_profile", e)
                education['organisation_profile'] = ''

            ## course details
            try:
                education['course_details'] = ''
                for text in block.css('h4 span::text').getall():
                    education['course_details'] = education['course_details'] + text.strip() + ' '
                education['course_details'] = education['course_details'].strip()
            except Exception as e:
                print("education --> course_details", e)
                education['course_details'] = ''

            ## description
            try:
                education['description'] = block.css('div.education__item--details p::text').get().strip()
            except Exception as e:
                print("education --> description", e)
                education['description'] = ''

         
            ## time range
            try:
                date_ranges = block.css('span.date-range time::text').getall()
                if len(date_ranges) == 2:
                    education['start_time'] = date_ranges[0]
                    education['end_time'] = date_ranges[1]
                elif len(date_ranges) == 1:
                    education['start_time'] = date_ranges[0]
                    education['end_time'] = 'present'
            except Exception as e:
                print("education --> time_ranges", e)
                education['start_time'] = ''
                education['end_time'] = ''

            item['education'].append(education)

        yield item
        
    

